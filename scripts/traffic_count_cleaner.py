import pandas as pd
from pathlib import Path


INPUT_FILE = Path("examples/sample_traffic_counts.csv")
OUTPUT_FILE = Path("outputs/traffic_count_summary.csv")


def clean_traffic_counts(input_file: Path, output_file: Path) -> None:
    """
    Read raw traffic count data, clean it, and export a summary by location and direction.
    """

    df = pd.read_csv(input_file)

    # Remove fully empty rows
    df = df.dropna(how="all")

    # Clean column names
    df.columns = df.columns.str.strip().str.lower()

    # Convert count column to numeric
    df["count"] = pd.to_numeric(df["count"], errors="coerce")

    # Remove rows with missing important values
    df = df.dropna(subset=["location", "direction", "count"])

    # Create summary
    summary = (
        df.groupby(["location", "direction"], as_index=False)["count"]
        .sum()
        .rename(columns={"count": "total_count"})
    )

    # Create output folder if it does not exist
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Export summary
    summary.to_csv(output_file, index=False)

    print(f"Summary saved to: {output_file}")


if __name__ == "__main__":
    clean_traffic_counts(INPUT_FILE, OUTPUT_FILE)
