# src/agents/data_agent.py

import pandas as pd
from pathlib import Path

class DataAgent:
    def __init__(self, data_path: str):
        self.data_path = Path(data_path)

    def load(self):
        df = pd.read_csv(self.data_path, parse_dates=["date"])
        return df

    def summarize_by_campaign_date(self, df):
        agg = df.groupby(["campaign_name", "date"]).agg({
            "spend": "sum",
            "impressions": "sum",
            "clicks": "sum",
            "purchases": "sum",
            "revenue": "sum",
        }).reset_index()

        # compute ctr & roas safely
        agg["ctr"] = agg["clicks"] / agg["impressions"].replace(0, pd.NA)
        agg["roas"] = agg["revenue"] / agg["spend"].replace(0, pd.NA)

        return agg
