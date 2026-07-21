.PHONY: all test clean
PYTHON ?= python3
all:
	$(PYTHON) src/run_pipeline.py
test:
	$(PYTHON) tests/test_outputs.py
clean:
	rm -f results/figures/*.png results/tables/*.csv results/tables/*.json
