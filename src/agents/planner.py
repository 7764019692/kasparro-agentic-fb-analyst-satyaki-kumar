# src/agents/planner.py

class PlannerAgent:
    def __init__(self):
        pass

    def plan(self, query: str):
        plan = {
            "task": "analyze_roas",
            "window_days": 7,
            "focus": "roas"
        }

        q = query.lower()

        # Check window
        if "14" in q or "last 14" in q:
            plan["window_days"] = 14

        # Check CTR
        if "ctr" in q:
            plan["focus"] = "ctr"

        return plan
