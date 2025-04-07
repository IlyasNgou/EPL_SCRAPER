# tests/test_basic.py

import sys
import os

# Add the project directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))


from main import extract_matches

def test_extract_matches_runs():
    try:
        extract_matches(1)  =
        assert True
    except Exception as e:
        assert False, f"Script failed with error: {e}"
