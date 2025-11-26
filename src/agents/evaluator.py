# src/agents/evaluator.py

class EvaluatorAgent:
    def __init__(self, min_confidence=0.5):
        self.min_confidence = min_confidence

    def validate(self, hypotheses, metrics):
        for h in hypotheses:
            evidence = h.get("evidence", {})

            pct_change = evidence.get("pct_change")
            if pct_change is not None and pct_change < -0.10:
                h["confidence"] = min(1.0, h["confidence"] + 0.1)

            ctr_change = metrics.get("ctr_change")
            if ctr_change is not None and ctr_change < -0.10:
                h["confidence"] = min(1.0, h["confidence"] + 0.12)

            if h["confidence"] < self.min_confidence:
                h["confidence"] = self.min_confidence

        return hypotheses
