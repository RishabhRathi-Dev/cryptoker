import pytest
from app import app

# pytest command is not working but test can be tested using python -m pytest tests/ commnad

def test_index_route():
    response = app.test_client().get('/')

    assert response.status_code == 200