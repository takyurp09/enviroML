# Learning journey: ten assignments, one analytical story

**Course:** MAST 638 — Machine Learning for Marine Science

**Instructor:** Dr. Yun Li

**Institution and term:** University of Delaware, Fall 2023

**Student:** Muhammad Taky Tahmid

The original course used sequential assignments. This portfolio presents them as stages of a single environmental-ML workflow rather than ten disconnected submissions.

| Stage | Original assignment title | Core skill | Portfolio role |
|---:|---|---|---|
| 1 | **DE River Estuary Chlorophyll-a** | MATLAB/NetCDF ingestion; arrays; spatial and temporal visualization | Establish the environmental signal and domain context |
| 2 | **Delaware Bay Chlorophyll-a and Environmental Predictors** | DataFrames; summary statistics; seasonal climatology | Build a tidy predictor/response dataset |
| 3 | **TSS in the Lower Delaware Bay** | Binning; outlier treatment; sensitivity analysis | Create explicit, auditable preprocessing rules |
| 4 | **Predict Chlorophyll a in the Lower Delaware Bay** | Data splitting; multiple and polynomial regression | Define the first supervised prediction task |
| 5 | **Classify the Subregions of the Delaware River Estuary** | Linear and nonlinear SVMs | Move from continuous prediction to ecological-region classification |
| 6 | **Model Evaluation for the Delaware River Estuary Subregion Classifier** | k-fold CV; learning/validation curves; grid search | Separate model selection from final evaluation |
| 7 | **The Classification of Data** | K-means; elbow and silhouette diagnostics | Discover water-quality regimes without labels |
| 8 | **Convolutional Neural Networks** | 2-D convolution; CNN training; image classification | Demonstrate deep-learning fundamentals and spatial feature extraction |
| 9 | **Classification and Regression of Data from the Delaware River Estuary** | Random forests; feature importance | Introduce nonlinear ensembles and interpretation |
| 10 | **Apply Ensemble Learning to the Data Analysis of Delaware River Estuary** | Voting, bagging, boosting | Compare complementary learners and ensemble logic |
| Capstone | **Predicting Air Temperature in Bangladesh Using Machine Learning Techniques** | ERA5; regularization; trees/boosting; sequence models | Transfer the workflow to a climate-prediction problem |

## Why the progression matters

The sequence demonstrates more than familiarity with model APIs. Early assignments establish environmental interpretation and data hygiene; middle assignments introduce supervised and unsupervised learning; later work emphasizes generalization, ensembles, and model diagnostics. The capstone then transfers those ideas to a distinct climate dataset.

## CNN evidence

HW08 was a discrete image-classification assignment rather than part of the estuary pipeline. Its original report is retained in the author's private course archive and is not redistributed here. It is listed as course evidence, but its performance is not mixed with the freshly rerun repository metrics.
