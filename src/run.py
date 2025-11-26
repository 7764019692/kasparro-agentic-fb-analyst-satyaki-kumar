# src/run.py - full orchestrator

import os, json, time
from pathlib import Path
from src.agents.data_agent import DataAgent
from src.agents.planner import PlannerAgent
from src.agents.insight_agent import InsightAgent
from src.agents.evaluator import EvaluatorAgent
from src.agents.creative_generator import CreativeGenerator

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data' / 'synthetic_fb_ads_undergarments.csv'
REPORTS = ROOT / 'reports'
LOGS = ROOT / 'logs'
REPORTS.mkdir(parents=True, exist_ok=True)
LOGS.mkdir(parents=True, exist_ok=True)

def write_log(name, payload):
    ts = int(time.time())
    p = LOGS / f"{name}_{ts}.json"
    with open(p, 'w', encoding='utf8') as f:
        json.dump(payload, f, indent=2)
    return str(p)

def analyze(query="Analyze ROAS drop", window_days=7):
    planner = PlannerAgent()
    plan = planner.plan(query)

    da = DataAgent(str(DATA))
    df = da.load()
    agg = da.summarize_by_campaign_date(df)
    campaigns = agg['campaign_name'].unique().tolist()

    insight_agent = InsightAgent()
    evaluator = EvaluatorAgent()
    creative_gen = CreativeGenerator()

    insights = []
    creatives = []

    for camp in campaigns:
        cdf = agg[agg['campaign_name'] == camp].sort_values('date')

        # Generate insights
        hypos = insight_agent.generate(cdf, window_days=window_days)

        # Metrics
        last_spend = float(cdf['spend'].tail(window_days).sum()) if len(cdf) > 0 else 0.0
        prev_spend = float(cdf['spend'].head(window_days).sum()) if len(cdf) > window_days else 0.0
        ctr_last = float(cdf['ctr'].tail(window_days).mean()) if 'ctr' in cdf else None
        ctr_prev = float(cdf['ctr'].head(window_days).mean()) if 'ctr' in cdf else None

        metrics = {'spend_last': last_spend, 'spend_prev': prev_spend}
        if ctr_last is not None and ctr_prev is not None:
            metrics['ctr_change'] = (ctr_last - ctr_prev) / (ctr_prev + 1e-9)

        # Evaluate hypotheses
        hypos = evaluator.validate(hypos, metrics)

        insights.append({
            'campaign_name': camp,
            'hypotheses': hypos,
            'metrics': metrics
        })

        # Creative suggestions
        messages = df[df['campaign_name'] == camp]['creative_message'].dropna().astype(str).tolist()
        suggestions = creative_gen.generate(messages, n=6)

        creatives.append({
            'campaign_name': camp,
            'suggestions': suggestions
        })

        # FIX: sanitize filename for Windows
        safe_name = "".join(c for c in camp if c.isalnum() or c in ("_", "-"))

        write_log(f"trace_{safe_name}", {
            'hypotheses': hypos,
            'metrics': metrics,
            'suggestions_sample': suggestions[:2]
        })

    # Save outputs
    with open(REPORTS / 'insights.json', 'w', encoding='utf8') as f:
        json.dump(insights, f, indent=2)

    with open(REPORTS / 'creatives.json', 'w', encoding='utf8') as f:
        json.dump(creatives, f, indent=2)

    with open(REPORTS / 'report.md', 'w', encoding='utf8') as f:
        f.write("# Automated Run\n\n")
        f.write(f"Generated insights for {len(campaigns)} campaigns.\n")

    print("Done: reports written to", REPORTS)


if __name__ == '__main__':
    analyze()
