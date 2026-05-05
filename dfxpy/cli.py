import argparse
import pandas as pd
import sys
from dfxpy import auto, eda, audit, prepare as prep

def main():
    parser = argparse.ArgumentParser(description="dfxpy: DataFrame Workflow Accelerator")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze a dataset")
    analyze_parser.add_argument("file", help="Path to CSV file")

    # Prepare command
    prepare_parser = subparsers.add_parser("prepare", help="Prepare a dataset for ML")
    prepare_parser.add_argument("file", help="Path to CSV file")
    prepare_parser.add_argument("--target", required=True, help="Target column name")
    prepare_parser.add_argument("--output", default="prepared_data.csv", help="Output path for X data")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    try:
        df = pd.read_csv(args.file)
    except Exception as e:
        print(f"Error loading file: {e}")
        sys.exit(1)

    if args.command == "analyze":
        print(f"Analyzing {args.file}...")
        df_clean = auto(df, verbose=True)
        eda(df_clean, verbose=True)
        audit(df_clean)

    elif args.command == "prepare":
        print(f"Preparing {args.file} with target '{args.target}'...")
        X, y = prep(df, target=args.target, verbose=True)
        # Save X for demonstration
        X.to_csv(args.output, index=False)
        print(f"Prepared features saved to {args.output}")

if __name__ == "__main__":
    main()
