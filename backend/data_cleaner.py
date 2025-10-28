import pandas as pd
import os

# Base paths
BASE_DIR = os.path.join(os.path.dirname(__file__), '..')
DATA_DIR = os.path.join(BASE_DIR, 'data')

def clean_file(input_filename, output_filename):
    raw_path = os.path.join(DATA_DIR, input_filename)
    cleaned_path = os.path.join(DATA_DIR, output_filename)

    if not os.path.exists(raw_path):
        print(f"⚠️ File not found: {raw_path}")
        return None

    df = pd.read_csv(raw_path)
    print(f"📥 Loaded {len(df)} records from {input_filename}")

    # --- Cleaning operations ---
    df.columns = [col.strip().replace(" ", "_").replace("(", "").replace(")", "") for col in df.columns]
    df.drop_duplicates(inplace=True)
    df.replace("#", pd.NA, inplace=True)

    # Convert date column
    if "Arrival_Date" in df.columns:
        df["Arrival_Date"] = pd.to_datetime(df["Arrival_Date"], errors='coerce')

    # Convert numeric columns
    for col in ["Min_Price", "Max_Price", "Modal_Price"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Drop missing key info
    df.dropna(subset=["State", "District", "Market", "Commodity"], inplace=True)

    # Save cleaned data
    df.to_csv(cleaned_path, index=False)
    print(f"✅ Cleaned data saved as {output_filename} ({len(df)} records)")
    return df


def clean_data():
    # Clean file1 if exists
    clean_file("file1.csv", "file1_cleaned.csv")

    # Clean file2 if exists
    clean_file("file2.csv", "file2_cleaned.csv")


if __name__ == "__main__":
    clean_data()
