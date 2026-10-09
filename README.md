# MP1 Data Pipeline

This project provides an end-to-end, configurable pipeline for loading, validating, cleaning, and saving tabular data. The root `pipeline.py` coordinates the workflow and command-line interface. The `src/data_loaders.py` module reads CSV, JSON, and YAML files, while `src/data_validator.py` checks required columns and removes invalid numeric values. The `src/data_processor.py` module applies the configured duplicate, missing-value, and outlier rules. The `src/data_output.py` module creates the destination directory and saves the cleaned data, and `src/utils.py` provides logging and input-path validation. Pipeline settings live in `config/config.yaml`, sample inputs live in `fixtures/`, and generated files are written under `output/`.

Run the completed pipeline with the provided sample data:

```bash
python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
```

This command creates `output/clean.csv` with 92 cleaned rows and prints a cleaning report.
