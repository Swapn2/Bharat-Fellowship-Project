import requests
import pandas as pd
import os

API_KEY = "579b464db66ec23bdd000001aba383b09a7b41147e89ca3f7418d315"
RESOURCE_ID = "35985678-0d79-46b4-9ed6-6f13308a1d24"
BASE_URL = f"https://api.data.gov.in/resource/{RESOURCE_ID}"

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(DATA_DIR, exist_ok=True)

# Keeps track of which slot (file1 or file2) to overwrite next
TRACKER_PATH = os.path.join(DATA_DIR, "fetch_tracker.txt")

def get_next_slot():
    """Alternate between file1 and file2."""
    if not os.path.exists(TRACKER_PATH):
        with open(TRACKER_PATH, "w") as f:
            f.write("1")
        return 1
    else:
        with open(TRACKER_PATH, "r+") as f:
            last = f.read().strip()
            next_slot = 2 if last == "1" else 1
            f.seek(0)
            f.write(str(next_slot))
            f.truncate()
        return next_slot


def fetch_all_data(state, district, commodity=None):
    all_records = []
    offset = 0
    limit = 1000

    print(f"Fetching data for {state} → {district} (Commodity: {commodity or 'All'})")

    while True:
        params = {
            "api-key": API_KEY,
            "format": "json",
            "limit": limit,
            "offset": offset,
            "filters[State]": state,
            "filters[District]": district,
        }

        if commodity:
            params["filters[Commodity]"] = commodity

        response = requests.get(BASE_URL, params=params)
        if response.status_code != 200:
            print(f"Request failed at offset {offset}: {response.status_code}")
            break

        data = response.json()
        records = data.get("records", [])
        if not records:
            break

        all_records.extend(records)
        print(f"Fetched {len(records)} records (Total: {len(all_records)})")

        if len(records) < limit:
            break
        offset += limit

    df = pd.DataFrame(all_records)
    if not df.empty:
        df.replace("#", pd.NA, inplace=True)

        slot = get_next_slot()
        csv_path = os.path.join(DATA_DIR, f"file{slot}.csv")
        df.to_csv(csv_path, index=False)

        print(f"✅ Saved {len(df)} records to {csv_path} (slot {slot})")
    else:
        print("⚠️ No data found for given filters.")

    return df


if __name__ == "__main__":
    state = input("Enter State: ").strip()
    district = input("Enter District: ").strip()
    commodity = input("Enter Commodity (or leave blank for all): ").strip() or None

    fetch_all_data(state, district, commodity)
