import pytest

from src.run import guard


def test_guard_blocks_draft_items_outside_smoke():
    with pytest.raises(SystemExit):
        guard({"items": "03_data/processed/pilot_items_draft.yaml"}, [])
    with pytest.raises(SystemExit):
        guard({"items": "x/pilot_items_draft.yaml", "smoke": True, "max_items": 30}, [])
    guard({"items": "x/pilot_items_draft.yaml", "smoke": True, "max_items": 2}, [])


def test_guard_blocks_test_split_without_frozen_protocol():
    with pytest.raises(SystemExit):
        guard({"items": "x/items_approved.yaml", "split": "test"}, [])
