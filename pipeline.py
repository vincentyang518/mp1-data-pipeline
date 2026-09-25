"""Command-line entry point for the MP1 data pipeline."""

import argparse
import logging
import sys
from pathlib import Path

from data_loaders import load_data


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def parse_args():
    """Parse command-line arguments for the data pipeline."""
    parser = argparse.ArgumentParser(description="Load and process a data file.")
    parser.add_argument(
        "--input",
        "-i",
        required=True,
        help="Path to the input data file",
    )
    parser.add_argument(
        "--output",
        "-o",
        required=True,
        help="Path for the cleaned output file",
    )
    parser.add_argument(
        "--format",
        choices=["csv", "json", "yaml"],
        default="csv",
        help="Output format (default: csv)",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed DEBUG messages",
    )
    return parser.parse_args()


def validate_input(filepath):
    """Return True when filepath points to an existing file."""
    path = Path(filepath)
    if not path.is_file():
        logger.error("Input file not found: %s", filepath)
        return False

    logger.info("Input file validated: %s", filepath)
    return True


def main():
    """Run the command-line data pipeline."""
    args = parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    logger.debug(
        "Arguments parsed: input=%s, output=%s format=%s",
        args.input,
        args.output,
        args.format,
    )

    if not validate_input(args.input):
        sys.exit(1)

    try:
        data = load_data(args.input)
    except ValueError:
        sys.exit(1)


if __name__ == "__main__":
    main()
