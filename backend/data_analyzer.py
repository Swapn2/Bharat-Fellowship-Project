import pandas as pd

def analyze_data(intent, cleaned_path):
    df = pd.read_csv(cleaned_path)

    if intent == "distinct_districts":
        return pd.DataFrame(df["District"].dropna().unique(), columns=["District"])
    elif intent == "distinct_markets":
        return pd.DataFrame(df["Market"].dropna().unique(), columns=["Market"])
    elif intent == "distinct_commodities":
        return pd.DataFrame(df["Commodity"].dropna().unique(), columns=["Commodity"])
    elif intent == "top_commodities":
        return df["Commodity"].value_counts().head(5).reset_index().rename(columns={"index": "Commodity", "Commodity": "Count"})
    elif intent == "mean_modal":
        return df.groupby("Commodity")["Modal_Price"].mean().reset_index().sort_values(by="Modal_Price", ascending=False)
    elif intent == "price_stats":
        return df.groupby("Commodity").agg(
            Min_Price_Min=("Min_Price", "min"),
            Max_Price_Max=("Max_Price", "max"),
            Mean_Modal_Price=("Modal_Price", "mean")
        ).reset_index()
    elif intent == "correlation":
        return df[["Min_Price", "Max_Price", "Modal_Price"]].corr()

    return "⚠️ Intent not recognized."
