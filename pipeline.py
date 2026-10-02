"""
Data Processing Pipeline

DS 3500 - MP1
"""

import argparse
import logging
import sys
from pathlib import Path

from data_loaders import load_data
from data_processor import create_cleaning_report, process_data


logger = logging.getLogger(__name__)


def setup_logging(verbose=False):
    """Configure logging for the pipeline."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
        datefmt="%H:%M:%S",
    )


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


def validate_input(filepath):
    """Check whether the input path exists and is a file."""
    path = Path(filepath)
    if not path.is_file():
        logger.error("Input file not found: %s", filepath)
        return False

    logger.info("Input file validated: %s", filepath)
    return True


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

    data_before = data.copy()
    try:
        cleaned_data = process_data(data, config)
    except ValueError:
        sys.exit(1)

    report = create_cleaning_report(data_before, cleaned_data)
    print(report)
    logger.info(
        "Processing complete: %d → %d rows",
        report["rows_before"],
        report["rows_after"],
    )
    cleaned_data.to_csv(args.output, index=False)
    logger.info("Saved cleaned data to %s", args.output)


if __name__ == "__main__":
    main()
