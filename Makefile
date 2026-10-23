PY := .venv/bin/python
EXP := cd 05_experiments &&

.PHONY: env test review-sheet smoke pilot analyze-pilot

env:            ## create the pinned environment
	uv venv --python 3.11 .venv && uv pip install --python $(PY) -r requirements.txt

test:           ## unit tests for normalisation, scoring and run guards
	$(EXP) ../$(PY) -m pytest -q

review-sheet:   ## regenerate author review sheets from the draft items
	$(EXP) ../$(PY) -m src.build_review_sheet ../03_data/processed/pilot_items_draft.yaml ../03_data/variants

smoke:          ## pipeline smoke test on 2 draft items (not a result)
	$(EXP) ../$(PY) -m src.run configs/smoke_qwen35_9b.yaml && ../$(PY) -m src.run configs/smoke_gemma2_9b.yaml

pilot:          ## G2 pilot (requires author-approved items)
	$(EXP) ../$(PY) -m src.run configs/pilot_qwen35_9b.yaml && ../$(PY) -m src.run configs/pilot_gemma2_9b.yaml

analyze-pilot:  ## score pilot runs -> 06_results/tables
	$(EXP) ../$(PY) -m src.analyze_pilot runs/$(RUN)
