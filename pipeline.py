"""
Data Processing Pipeline

DS 3500 - MP1
"""

import argparse
import logging
import sys

from src import (
    create_cleaning_report,
    load_data,
    process_data,
    save_data,
    setup_logging,
    validate_dataframe,
    validate_input,
)


logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Load and process a data file.")
    parser.add_argument(
        "--input",
        "-i",
        required=True,
        help="Path to the input data file",
    )
    parser.add_argument(
        "--config",
        "-c",
        required=True,
        help="Path to the YAML configuration file",
    )
    parser.add_argument(
        "--output",
        "-o",
        required=True,
        help="Path for the cleaned output file",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed DEBUG messages",
    )
    return parser.parse_args()


def main():
    """Main pipeline function."""
    args = parse_arguments()
    setup_logging(args.verbose)

    logger.debug(
        "Arguments parsed: input=%s, config=%s, output=%s",
        args.input,
        args.config,
        args.output,
    )

    if not validate_input(args.input):
        sys.exit(1)
    if not validate_input(args.config):
        sys.exit(1)

    try:
        data = load_data(args.input)
        config = load_data(args.config)
    except ValueError:
        sys.exit(1)

    validation = config["validation"]
    rows_before_validation = len(data)
    try:
        validated_data = validate_dataframe(
            data,
            validation["required_columns"],
            validation["numeric_columns"],
        )
    except ValueError:
        sys.exit(1)

    logger.info(
        "Validation complete: %d → %d rows",
        rows_before_validation,
        len(validated_data),
    )

    data_before = validated_data.copy()
    try:
        cleaned_data = process_data(validated_data, config)
    except ValueError:
        sys.exit(1)

    report = create_cleaning_report(data_before, cleaned_data)
    logger.info(
        "Processing complete: %d → %d rows",
        report["rows_before"],
        report["rows_after"],
    )
    output_path = save_data(cleaned_data, args.output)
    logger.info("Saved cleaned data to %s", output_path)

    print("Cleaning report:")
    print(report)


if __name__ == "__main__":
    main()
