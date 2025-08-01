import argparse

from src.partition.run_partition import run_partition
from src.merge.run_merge import run_merge


def get_arguments(argv=None):
    """Parse command line arguments for cutting or merging geometries."""
    
    # Common parser for shared arguments
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument("--area_id", type=str, nargs="+", required=True,
                                help="List of ID prefixes of the areas to cut or merge (e.g. --area_id 143 1478 1479)")
    common_parser.add_argument("--min_addresses", type=float, required=True, help="Minimum number of addresses per piece")
    common_parser.add_argument('--avg', action='store_true', help='Count addresses as daily average instead of total.')
    common_parser.add_argument("--teryt_id", type=str, default=None, help="Optional TERYT ID to filter addresses")
    common_parser.add_argument("--config", type=str, default="db_config.json",
                        help="Path to config file (default: arc/handle_database/config.json)")
    common_parser.add_argument("--output_table", type=str, default=None,
                    help="Name of the output table to save partition results (default: specified in config)")

    parser = argparse.ArgumentParser(description="Cut or merge geometries by area ID using OSM data and weights")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Action to perform: cut or merge")

    # Additional arguments for cut command
    cut_parser = subparsers.add_parser("cut", help="Cut geometries into smaller pieces", parents=[common_parser])
    cut_parser.add_argument("--weights_path", type=str, default=None, help="Path to the weights CSV file (default: specified config)")
    cut_parser.set_defaults(func=run_partition)
    
    # Additional arguments for merge command
    merge_parser = subparsers.add_parser("merge", help="Merge geometries based on shortest route", parents=[common_parser])
    merge_parser.add_argument("--max_addresses", type=float, required=True,
                              help="Maximum number of addresses (daily average from time period specified in config) allowed in a merged polygon")
    merge_parser.set_defaults(func=run_merge)
    
    return parser.parse_args(argv)


def main():

    args = get_arguments()
    args.func(args)


if __name__ == "__main__":
    main()