import pytest
from unittest.mock import patch, MagicMock
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from app import app, moving_average


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# --------------------------
# Unit Tests for moving_average
# --------------------------
def test_moving_average_with_enough_data():
    prices = [100, 110, 120]
    result = moving_average(prices, window=3)
    assert result == 110  # (100+110+120)/3


def test_moving_average_with_insufficient_data():
    prices = [100, 110]
    result = moving_average(prices, window=3)
    assert result is None


# --------------------------
# API Tests (/stocks)
# --------------------------
@patch("app.get_db_connection")
def test_get_stocks_success(mock_db, client):
    # Mock DB rows
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [
        {"id": 1, "ticker": "AAPL", "price": 150, "date": "2025-10-01"},
        {"id": 2, "ticker": "MSFT", "price": 300, "date": "2025-10-02"},
    ]
    mock_db.return_value.cursor.return_value = mock_cursor

    response = client.get("/stocks")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert data[0]["ticker"] == "AAPL"


@patch("app.get_db_connection")
def test_get_stocks_db_error(mock_db, client):
    mock_db.side_effect = Exception("DB error")

    response = client.get("/stocks")
    assert response.status_code == 500
    assert "error" in response.get_json()


# --------------------------
# API Tests (/predict)
# --------------------------
@patch("app.get_db_connection")
def test_predict_success(mock_db, client):
    # Mock last 3 prices for ticker AAPL
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [(100,), (110,), (120,)]
    mock_db.return_value.cursor.return_value = mock_cursor

    response = client.get("/predict?ticker=AAPL")
    assert response.status_code == 200
    data = response.get_json()
    assert data["ticker"] == "AAPL"
    assert data["last_prices"] == [100, 110, 120]
    assert data["predicted_price"] == 110.0


@patch("app.get_db_connection")
def test_predict_not_enough_data(mock_db, client):
    # Mock only 2 rows returned
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [(100,), (110,)]
    mock_db.return_value.cursor.return_value = mock_cursor

    response = client.get("/predict?ticker=AAPL")
    assert response.status_code == 400
    assert "error" in response.get_json()


@patch("app.get_db_connection")
def test_predict_db_error(mock_db, client):
    mock_db.side_effect = Exception("DB connection failed")

    response = client.get("/predict?ticker=AAPL")
    assert response.status_code == 500
    assert "error" in response.get_json()
