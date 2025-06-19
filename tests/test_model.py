import pandas as pd
import pytest

from backend.model import train_and_predict, MIN_REQUIRED_ROWS


def test_train_and_predict_small_dataframe_raises_value_error():
    df = pd.DataFrame({'close': range(5)})
    with pytest.raises(ValueError, match=str(MIN_REQUIRED_ROWS)):
        train_and_predict(df)
