import pandas as pd
import pytest

from backend.model import train_and_predict, MIN_REQUIRED_ROWS


def test_train_and_predict_small_dataframe_raises_value_error():
    df = pd.DataFrame({'close': range(5)})
    with pytest.raises(ValueError, match=str(MIN_REQUIRED_ROWS)):
        train_and_predict(df)


def test_train_and_predict_returns_metrics():
    df = pd.DataFrame({'close': range(MIN_REQUIRED_ROWS + 10)})
    result = train_and_predict(df)
    assert 'prediction' in result
    assert 'plot_base64' in result
    assert 'r2' in result
    assert 'mae' in result
    assert 'rmse' in result
    assert 'importance_plot_base64' in result
