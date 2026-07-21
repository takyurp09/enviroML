"""Reproducible enviroML pipeline for environmental ML case studies."""
from pathlib import Path
import json, warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.ensemble import (GradientBoostingClassifier, RandomForestClassifier,
                              RandomForestRegressor, VotingClassifier, VotingRegressor,
                              HistGradientBoostingRegressor)
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge
from sklearn.metrics import (ConfusionMatrixDisplay, accuracy_score, adjusted_rand_score,
                             balanced_accuracy_score, mean_absolute_error,
                             mean_squared_error, r2_score, silhouette_score)
from sklearn.model_selection import (GridSearchCV, GroupKFold, RepeatedStratifiedKFold,
                                     TimeSeriesSplit, cross_validate, train_test_split)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

warnings.filterwarnings("ignore", category=RuntimeWarning)
ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "results" / "figures"
TAB = ROOT / "results" / "tables"
FIG.mkdir(parents=True, exist_ok=True); TAB.mkdir(parents=True, exist_ok=True)
SEED = 638
FEATURES = ["water_temp_value", "ph_value", "salinity_value",
            "nutrient_nitrogen_value", "phosphate_phosphorus_value",
            "tss_value", "do_value"]
REGIONS = {
    "091002":"Estuarine Turbidity Maximum", "091005":"Estuarine Turbidity Maximum",
    "091008":"Estuarine Turbidity Maximum", "091011":"Estuarine Turbidity Maximum",
    "091015":"Estuarine Turbidity Maximum", "091017":"Estuarine Turbidity Maximum",
    "091020":"Transitional", "091023":"Bay", "091026":"Bay", "091028":"Bay",
    "091030":"Bay", "332046":"Upper River", "332049":"Upper River",
    "332052":"Upper River", "892062":"Upper River", "892065":"Upper River",
    "892070":"Upper River", "892071":"Upper River", "892077":"Upper River",
}

def style():
    plt.rcParams.update({"figure.dpi":140,"savefig.dpi":180,"font.size":9,
        "axes.spines.top":False,"axes.spines.right":False,"axes.titleweight":"bold",
        "axes.facecolor":"#f8fafc","figure.facecolor":"white","grid.alpha":.22})

def load_estuary():
    frames=[]
    for f in sorted((ROOT/"data/raw/estuary").glob("station-*.csv")):
        if f.stat().st_size < 100: continue
        d=pd.read_csv(f); d["station"]=f.stem.replace("station-","")
        frames.append(d)
    d=pd.concat(frames, ignore_index=True)
    d["timestamp"]=pd.to_datetime(d["timestamp"], errors="coerce")
    for c in FEATURES+["chlora_value"]: d[c]=pd.to_numeric(d[c], errors="coerce")
    d["region"]=d["station"].map(REGIONS)
    # Physically plausible screens; imputation occurs inside each fitted pipeline.
    bounds={"water_temp_value":(-3,40),"ph_value":(4,11),"salinity_value":(0,40),
            "nutrient_nitrogen_value":(0,20),"phosphate_phosphorus_value":(0,5),
            "tss_value":(0,1000),"do_value":(0,25),"chlora_value":(0,500)}
    for c,(lo,hi) in bounds.items(): d.loc[~d[c].between(lo,hi),c]=np.nan
    return d

def eda(d):
    q=pd.DataFrame({"variable":FEATURES+["chlora_value"],
                    "n_valid":[d[c].notna().sum() for c in FEATURES+["chlora_value"]],
                    "missing_pct":[100*d[c].isna().mean() for c in FEATURES+["chlora_value"]],
                    "median":[d[c].median() for c in FEATURES+["chlora_value"]]})
    q.to_csv(TAB/"01_data_quality.csv",index=False)
    monthly=d.assign(month=d.timestamp.dt.month).groupby("month").chlora_value.agg(["median","count"])
    fig,ax=plt.subplots(figsize=(8,4)); ax.plot(monthly.index,monthly["median"],marker="o",color="#087e8b",lw=2)
    ax.fill_between(monthly.index,0,monthly["median"],alpha=.12,color="#087e8b")
    ax.set(xticks=range(1,13),xlabel="Month",ylabel="Median chlorophyll-a (µg/L)",
           title="Seasonal chlorophyll signal across Delaware Estuary stations")
    ax.grid(axis="y"); fig.tight_layout(); fig.savefig(FIG/"01_seasonal_signal.png"); plt.close(fig)

def regression(d):
    x=d.loc[d.chlora_value.notna(),FEATURES]; y=d.loc[d.chlora_value.notna(),"chlora_value"]
    Xtr,Xte,ytr,yte=train_test_split(x,y,test_size=.25,random_state=SEED)
    models={
      "Linear":Pipeline([("imp",SimpleImputer()),("scale",StandardScaler()),("m",LinearRegression())]),
      "Ridge":Pipeline([("imp",SimpleImputer()),("scale",StandardScaler()),("m",Ridge(alpha=10))]),
      "Random forest":Pipeline([("imp",SimpleImputer()),("m",RandomForestRegressor(n_estimators=350,min_samples_leaf=4,random_state=SEED,n_jobs=1))])}
    rows=[]; preds={}
    for name,m in models.items():
        m.fit(Xtr,ytr); p=m.predict(Xte); preds[name]=p
        rows.append({"model":name,"MAE":mean_absolute_error(yte,p),"RMSE":mean_squared_error(yte,p)**.5,"R2":r2_score(yte,p)})
    ensemble=VotingRegressor([("ridge",models["Ridge"]),("rf",models["Random forest"])])
    ensemble.fit(Xtr,ytr); p=ensemble.predict(Xte); preds["Voting ensemble"]=p
    rows.append({"model":"Voting ensemble","MAE":mean_absolute_error(yte,p),"RMSE":mean_squared_error(yte,p)**.5,"R2":r2_score(yte,p)})
    out=pd.DataFrame(rows).sort_values("RMSE"); out.to_csv(TAB/"02_regression_comparison.csv",index=False)
    best=out.iloc[0].model; p=preds[best]
    fig,ax=plt.subplots(figsize=(5.4,5)); ax.scatter(yte,p,s=16,alpha=.45,color="#087e8b",edgecolor="none")
    lim=max(np.nanpercentile(yte,99),np.nanpercentile(p,99)); ax.plot([0,lim],[0,lim],"--",color="#f97316")
    ax.set(xlim=(0,lim),ylim=(0,lim),xlabel="Observed chlorophyll-a (µg/L)",ylabel="Predicted chlorophyll-a (µg/L)",
           title=f"Held-out regression: {best}")
    ax.text(.04,.94,f"RMSE = {out.iloc[0].RMSE:.2f}\nR² = {out.iloc[0].R2:.2f}",transform=ax.transAxes,va="top")
    fig.tight_layout(); fig.savefig(FIG/"02_regression_validation.png"); plt.close(fig)
    return out.iloc[0].to_dict()

def classification(d):
    z=d[d.region.notna()].dropna(subset=["region"]); X=z[FEATURES]; y=z.region
    Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.25,stratify=y,random_state=SEED)
    prep=[("imp",SimpleImputer()),("scale",StandardScaler())]
    svc=GridSearchCV(Pipeline(prep+[("m",SVC(probability=True,class_weight="balanced",random_state=SEED))]),
                     {"m__C":[.1,1,10,100],"m__gamma":["scale",.01,.1],"m__kernel":["rbf"]},cv=5,scoring="balanced_accuracy",n_jobs=1)
    candidates={"Logistic":Pipeline(prep+[("m",LogisticRegression(max_iter=3000,class_weight="balanced",random_state=SEED))]),
      "Tuned SVM":svc,
      "Random forest":Pipeline([("imp",SimpleImputer()),("m",RandomForestClassifier(n_estimators=350,min_samples_leaf=3,class_weight="balanced",random_state=SEED,n_jobs=1))]),
      "Gradient boosting":Pipeline([("imp",SimpleImputer()),("m",GradientBoostingClassifier(random_state=SEED))])}
    candidates["Soft-voting ensemble"]=VotingClassifier(
        [("logistic",candidates["Logistic"]),("svm",Pipeline(prep+[("m",SVC(C=10,gamma="scale",probability=True,class_weight="balanced",random_state=SEED))])),("rf",candidates["Random forest"])],
        voting="soft")
    cv=RepeatedStratifiedKFold(n_splits=5,n_repeats=2,random_state=SEED); rows=[]
    for name,m in candidates.items():
        sc=cross_validate(m,Xtr,ytr,cv=cv,scoring=["accuracy","balanced_accuracy"],n_jobs=1)
        m.fit(Xtr,ytr); p=m.predict(Xte)
        rows.append({"model":name,"cv_balanced_accuracy_mean":sc["test_balanced_accuracy"].mean(),
                     "cv_balanced_accuracy_sd":sc["test_balanced_accuracy"].std(),
                     "test_accuracy":accuracy_score(yte,p),"test_balanced_accuracy":balanced_accuracy_score(yte,p)})
    out=pd.DataFrame(rows).sort_values("test_balanced_accuracy",ascending=False); out.to_csv(TAB/"03_classification_comparison.csv",index=False)
    best_name=out.iloc[0].model; best=candidates[best_name]; best.fit(Xtr,ytr); pred=best.predict(Xte)
    fig,ax=plt.subplots(figsize=(7,5)); ConfusionMatrixDisplay.from_predictions(yte,pred,normalize="true",cmap="Blues",ax=ax,colorbar=False)
    ax.set_title(f"Held-out region classification: {best_name}\n(row-normalized)"); fig.tight_layout(); fig.savefig(FIG/"03_confusion_matrix.png"); plt.close(fig)
    rf=candidates["Random forest"].fit(Xtr,ytr); pi=permutation_importance(rf,Xte,yte,n_repeats=15,random_state=SEED,scoring="balanced_accuracy")
    imp=pd.DataFrame({"feature":FEATURES,"importance":pi.importances_mean,"sd":pi.importances_std}).sort_values("importance")
    imp.to_csv(TAB/"04_permutation_importance.csv",index=False)
    fig,ax=plt.subplots(figsize=(7,4.5)); ax.barh(imp.feature.str.replace("_value",""),imp.importance,xerr=imp.sd,color="#087e8b",alpha=.9)
    ax.set(xlabel="Decrease in held-out balanced accuracy",title="Random-forest permutation importance"); ax.grid(axis="x")
    fig.tight_layout(); fig.savefig(FIG/"04_feature_importance.png"); plt.close(fig)
    return out.iloc[0].to_dict()

def robust_validation(d):
    """Spatial/temporal validation, uncertainty intervals, and subgroup errors."""
    z=d[d.chlora_value.notna()].copy(); X=z[FEATURES]; y=z.chlora_value; groups=z.station
    rf=Pipeline([("imp",SimpleImputer()),("m",RandomForestRegressor(n_estimators=200,min_samples_leaf=4,random_state=SEED,n_jobs=1))])
    rows=[]; residual_parts=[]
    for fold,(tr,te) in enumerate(GroupKFold(5).split(X,y,groups),1):
        rf.fit(X.iloc[tr],y.iloc[tr]); p=rf.predict(X.iloc[te]); e=y.iloc[te]-p
        rows.append({"design":"station-held-out","fold":fold,"n_test":len(te),"RMSE":mean_squared_error(y.iloc[te],p)**.5,"MAE":mean_absolute_error(y.iloc[te],p),"R2":r2_score(y.iloc[te],p)})
        residual_parts.append(pd.DataFrame({"station":z.station.iloc[te],"timestamp":z.timestamp.iloc[te],"observed":y.iloc[te],"predicted":p,"residual":e}))
    years=sorted(z.timestamp.dt.year.dropna().unique()); cutoff=years[int(.70*len(years))-1]
    tr=z.timestamp.dt.year<=cutoff; te=z.timestamp.dt.year>cutoff; rf.fit(X[tr],y[tr]); p=rf.predict(X[te]); e=y[te]-p
    rows.append({"design":f"temporal: <= {cutoff} vs > {cutoff}","fold":1,"n_test":int(te.sum()),"RMSE":mean_squared_error(y[te],p)**.5,"MAE":mean_absolute_error(y[te],p),"R2":r2_score(y[te],p)})
    residual_parts.append(pd.DataFrame({"station":z.station[te],"timestamp":z.timestamp[te],"observed":y[te],"predicted":p,"residual":e}))
    pd.DataFrame(rows).to_csv(TAB/"08_spatiotemporal_validation.csv",index=False)
    res=pd.concat(residual_parts,ignore_index=True); res["absolute_error"]=res.residual.abs(); res["season"]=pd.cut(res.timestamp.dt.month,[0,2,5,8,11,12],labels=["Winter","Spring","Summer","Autumn","Winter2"]); res["season"]=res.season.astype(str).replace("Winter2","Winter")
    by_season=res.groupby("season",as_index=False).agg(n=("residual","size"),MAE=("absolute_error","mean"),bias=("residual","mean")); by_season.to_csv(TAB/"09_error_by_season.csv",index=False)
    rng=np.random.default_rng(SEED); vals=[]; obs=y[te].to_numpy(); pred=p
    for _ in range(1000):
        ix=rng.integers(0,len(obs),len(obs)); vals.append(mean_squared_error(obs[ix],pred[ix])**.5)
    ci=pd.DataFrame({"metric":["temporal_test_RMSE"],"estimate":[mean_squared_error(obs,pred)**.5],"lower_95":[np.quantile(vals,.025)],"upper_95":[np.quantile(vals,.975)],"bootstrap_reps":[1000]}); ci.to_csv(TAB/"10_uncertainty_intervals.csv",index=False)
    fig,axs=plt.subplots(1,2,figsize=(10,4)); spatial=pd.DataFrame(rows[:5]); axs[0].bar(spatial.fold,spatial.RMSE,color="#087e8b"); axs[0].axhline(spatial.RMSE.mean(),ls="--",color="#f97316"); axs[0].set(xlabel="Held-out station fold",ylabel="RMSE (µg/L)",title="Generalization to unseen stations")
    axs[1].bar(by_season.season,by_season.MAE,color="#315c7d"); axs[1].set(xlabel="Season",ylabel="MAE (µg/L)",title="Error analysis by season");
    for ax in axs: ax.grid(axis="y"); fig.tight_layout(); fig.savefig(FIG/"07_spatiotemporal_validation.png"); plt.close(fig)
    return {"station_cv_RMSE_mean":float(spatial.RMSE.mean()),"temporal_RMSE":float(rows[-1]["RMSE"]),"temporal_RMSE_CI":[float(ci.lower_95.iloc[0]),float(ci.upper_95.iloc[0])]}

def station_map(d):
    coords=pd.read_csv(ROOT/"data/station_coordinates.csv",dtype={"station":str}); stats=d.groupby("station",as_index=False).agg(median_chla=("chlora_value","median"),n=("chlora_value","count")); m=coords.merge(stats,on="station",how="left"); m["region"]=m.station.map(REGIONS).fillna("Upper River")
    m.to_csv(TAB/"11_station_map_data.csv",index=False); colors={"Bay":"#0077b6","Transitional":"#7b2cbf","Estuarine Turbidity Maximum":"#f97316","Upper River":"#2a9d8f"}
    fig,ax=plt.subplots(figsize=(7.4,8)); ax.plot(m.longitude,m.latitude,color="#8ecae6",lw=7,alpha=.28,zorder=1)
    for region,g in m.groupby("region"):
        s=40+5*np.sqrt(g.n.fillna(0)); ax.scatter(g.longitude,g.latitude,s=s,c=colors[region],label=region,edgecolor="white",linewidth=.8,zorder=3)
    for i,(_,r) in enumerate(m.iterrows()): ax.annotate(r.station,(r.longitude,r.latitude),xytext=(5,4 if i%2 else -5),textcoords="offset points",fontsize=7,va="center")
    ax.set(xlabel="Longitude",ylabel="Latitude",title="Delaware Estuary water-quality monitoring network"); ax.legend(frameon=True,framealpha=.92,title="Course-defined region",loc="upper left",fontsize=8); ax.grid(); ax.set_aspect(1/np.cos(np.deg2rad(m.latitude.mean())))
    fig.tight_layout(); fig.savefig(FIG/"08_station_network_map.png"); plt.close(fig)


def clustering(d):
    station=d.groupby("station")[FEATURES+["chlora_value"]].median().dropna(thresh=5)
    X=SimpleImputer().fit_transform(station); X=StandardScaler().fit_transform(X)
    rows=[]
    for k in range(2,7):
        lab=KMeans(k,random_state=SEED,n_init=50).fit_predict(X)
        rows.append({"k":k,"silhouette":silhouette_score(X,lab)})
    scores=pd.DataFrame(rows); scores.to_csv(TAB/"05_cluster_selection.csv",index=False); k=int(scores.loc[scores.silhouette.idxmax(),"k"])
    base=KMeans(k,random_state=SEED,n_init=50).fit_predict(X); aris=[]; rng=np.random.default_rng(SEED)
    for b in range(200):
        cols=rng.choice(X.shape[1],X.shape[1],replace=True); lab=KMeans(k,random_state=SEED+b,n_init=20).fit_predict(X[:,cols]); aris.append(adjusted_rand_score(base,lab))
    pd.DataFrame({"bootstrap_ARI":aris}).to_csv(TAB/"06_cluster_stability.csv",index=False)
    fig,axs=plt.subplots(1,2,figsize=(9,3.8)); axs[0].plot(scores.k,scores.silhouette,marker="o",color="#087e8b"); axs[0].set(xlabel="Number of clusters",ylabel="Silhouette score",title="Cluster model selection")
    axs[1].hist(aris,bins=15,color="#f97316",alpha=.8); axs[1].axvline(np.median(aris),color="#172554",ls="--"); axs[1].set(xlabel="Adjusted Rand index",ylabel="Bootstrap runs",title="Feature-bootstrap stability")
    for ax in axs: ax.grid(alpha=.2); fig.tight_layout(); fig.savefig(FIG/"05_clustering_diagnostics.png"); plt.close(fig)
    return {"selected_k":k,"silhouette":float(scores.silhouette.max()),"median_bootstrap_ARI":float(np.median(aris))}

def climate():
    f=ROOT/"data/raw/climate/era5_bangladesh_2000.csv"; d=pd.read_csv(f); d["time"]=pd.to_datetime(d.time)
    d=d.sort_values("time"); d["hour_sin"]=np.sin(2*np.pi*d.time.dt.hour/24); d["hour_cos"]=np.cos(2*np.pi*d.time.dt.hour/24)
    d["doy_sin"]=np.sin(2*np.pi*d.time.dt.dayofyear/366); d["doy_cos"]=np.cos(2*np.pi*d.time.dt.dayofyear/366)
    feats=[c for c in ["longitude","latitude","u10","v10","e","ssr","sp","tp","hour_sin","hour_cos","doy_sin","doy_cos"] if c in d]
    d=d.dropna(subset=feats+["t2m"]).sort_values(["time","latitude","longitude"]); times=np.sort(d.time.unique()); cut=times[int(.75*len(times))]; tr=d.time<cut; te=~tr; Xtr,Xte=d.loc[tr,feats],d.loc[te,feats]; ytr=d.loc[tr,"t2m"]-273.15; yte=d.loc[te,"t2m"]-273.15
    models={"Seasonal linear":Pipeline([("imp",SimpleImputer()),("scale",StandardScaler()),("m",Ridge(alpha=1))]),
            "Histogram gradient boosting":Pipeline([("imp",SimpleImputer()),("m",HistGradientBoostingRegressor(max_iter=150,l2_regularization=1,random_state=SEED))])}
    rows=[]; preds={}
    for n,m in models.items(): m.fit(Xtr,ytr); p=m.predict(Xte); preds[n]=p; rows.append({"model":n,"MAE_C":mean_absolute_error(yte,p),"RMSE_C":mean_squared_error(yte,p)**.5,"R2":r2_score(yte,p)})
    train=d.loc[tr].copy(); test=d.loc[te].copy(); train["temp_C"]=ytr.values; climatology=train.groupby([train.time.dt.month,train.time.dt.hour]).temp_C.mean(); keys=list(zip(test.time.dt.month,test.time.dt.hour)); cp=np.array([climatology.get(k,ytr.mean()) for k in keys]); rows.append({"model":"Monthly-hour climatology","MAE_C":mean_absolute_error(yte,cp),"RMSE_C":mean_squared_error(yte,cp)**.5,"R2":r2_score(yte,cp)}); preds["Monthly-hour climatology"]=cp
    d["persistence_C"]=d.groupby(["longitude","latitude"]).t2m.shift(1)-273.15; pp=d.loc[te,"persistence_C"]; ok=pp.notna(); rows.append({"model":"Persistence baseline","MAE_C":mean_absolute_error(yte[ok],pp[ok]),"RMSE_C":mean_squared_error(yte[ok],pp[ok])**.5,"R2":r2_score(yte[ok],pp[ok])}); preds["Persistence baseline"]=pp.to_numpy()
    out=pd.DataFrame(rows).sort_values("RMSE_C"); out.to_csv(TAB/"07_climate_time_split.csv",index=False); best=out.iloc[0].model
    # Plot the spatial mean to keep the dense grid legible.
    plot=pd.DataFrame({"time":test.time.values,"observed":yte.values,"predicted":preds[best]}).groupby("time",as_index=False).mean()
    fig,ax=plt.subplots(figsize=(10,4)); ax.plot(plot.time,plot.observed,color="#94a3b8",lw=.9,label="ERA5 observed"); ax.plot(plot.time,plot.predicted,color="#087e8b",lw=.9,label=best)
    ax.set(xlabel="Held-out final quarter of 2000",ylabel="2 m temperature (°C)",title="Bangladesh temperature prediction with chronological validation"); ax.legend(frameon=False,ncol=2); ax.grid(axis="y")
    fig.tight_layout(); fig.savefig(FIG/"06_climate_time_validation.png"); plt.close(fig)
    err=test[["longitude","latitude"]].copy(); err["sq_error"]=(yte.values-preds[best])**2; grid=err.groupby(["longitude","latitude"],as_index=False).sq_error.mean(); grid["RMSE_C"]=np.sqrt(grid.sq_error); grid.to_csv(TAB/"12_climate_spatial_error.csv",index=False)
    fig,ax=plt.subplots(figsize=(7,5.5)); sc=ax.scatter(grid.longitude,grid.latitude,c=grid.RMSE_C,s=75,cmap="magma",marker="s"); fig.colorbar(sc,ax=ax,label="Held-out RMSE (°C)"); ax.set(xlabel="Longitude",ylabel="Latitude",title="Spatial distribution of Bangladesh prediction error"); ax.grid(); fig.tight_layout(); fig.savefig(FIG/"09_climate_error_map.png"); plt.close(fig)
    # Expanding-window validation on spatially averaged time steps.
    avg=d.groupby("time",as_index=False)[feats+["t2m"]].mean(); Xc=avg[feats]; yc=avg.t2m-273.15; cvrows=[]
    for fold,(a,b) in enumerate(TimeSeriesSplit(5).split(Xc),1):
        model=models["Seasonal linear"].fit(Xc.iloc[a],yc.iloc[a]); pr=model.predict(Xc.iloc[b]); cvrows.append({"fold":fold,"train_n":len(a),"test_n":len(b),"RMSE_C":mean_squared_error(yc.iloc[b],pr)**.5,"MAE_C":mean_absolute_error(yc.iloc[b],pr)})
    pd.DataFrame(cvrows).to_csv(TAB/"13_climate_timeseries_cv.csv",index=False)
    return out.iloc[0].to_dict()

def main():
    style(); d=load_estuary(); eda(d)
    station_map(d)
    summary={"records":len(d),"stations":d.station.nunique(),"regression":regression(d),
             "classification":classification(d),"clustering":clustering(d),
             "robust_validation":robust_validation(d),"climate":climate()}
    (TAB/"project_summary.json").write_text(json.dumps(summary,indent=2,default=float))
    print(json.dumps(summary,indent=2,default=float))

if __name__ == "__main__": main()
