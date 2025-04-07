# tests/test_basic.py

from main_script import extract_matches

def test_extract_matches_runs():
    try:
        extract_matches(1)  
        assert True
    except Exception as e:
        assert False, f"Script failed with error: {e}"
