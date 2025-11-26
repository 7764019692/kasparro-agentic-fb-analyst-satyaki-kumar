# src/agents/insight_agent.py

import numpy as np

class InsightAgent:
    def __init__(self, min_pct_drop=0.15):
        self.min_pct_drop = min_pct_drop

    def generate(self, campaign_df, window_days=7):
        if len(campaign_df) == 0:
            return [{
                "hypothesis": "No data",
                "reasoning": "Campaign dataframe is empty",
                "confidence": 0.2
            }]

        last_mean = campaign_df["roas"].tail(window_days).mean()
        prev_mean = campaign_df["roas"].head(window_days).mean()
        pct_change = (last_mean - prev_mean) / (prev_mean + 1e-9)

        insights = []

        if pct_change < -self.min_pct_drop:
            insights.append({
                "hypothesis": "ROAS dropped significantly",
                "reasoning": f"ROAS decreased by {pct_change:.2%}",
                "confidence": min(1.0, 0.6 + abs(pct_change)),
                "evidence": {
                    "last_mean": float(last_mean),
                    "prev_mean": float(prev_mean),
                    "pct_change": float(pct_change)
                }
            })

        if "ctr" in campaign_df.columns:
            ctr_last = campaign_df["ctr"].tail(window_days).mean()
            ctr_prev = campaign_df["ctr"].head(window_days).mean()
            ctr_change = (ctr_last - ctr_prev) / (ctr_prev + 1e-9)

            if ctr_change < -0.10:
                insights.append({
                    "hypothesis": "CTR dropped — likely creative fatigue",
                    "reasoning": f"CTR decreased by {ctr_change:.2%}",
                    "confidence": 0.5 + abs(ctr_change),
                    "evidence": {
                        "ctr_last": float(ctr_last),
                        "ctr_prev": float(ctr_prev),
                        "ctr_change": float(ctr_change)
                    }
                })

        if not insights:
            insights.append({
                "hypothesis": "Performance stable",
                "reasoning": "No major ROAS or CTR changes",
                "confidence": 0.5
            })

        return insights
