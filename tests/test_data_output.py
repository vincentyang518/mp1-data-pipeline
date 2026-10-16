import pandas as pd

from src import save_data


def test_save_data_creates_csv(sample_df, tmp_path):
    output_path = tmp_path / "clean.csv"

    result = save_data(sample_df, output_path)
    saved_df = pd.read_csv(output_path)

    assert result == output_path
    assert len(saved_df) == len(sample_df)
    assert list(saved_df.columns) == list(sample_df.columns)
