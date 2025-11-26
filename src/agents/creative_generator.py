# src/agents/creative_generator.py

from collections import Counter
import re, uuid

def tokenize(text):
    if not text:
        return []
    return re.findall(r"[A-Za-z']{2,}", text.lower())

class CreativeGenerator:
    def __init__(self):
        pass

    def generate(self, messages, n=6):
        tokens = []
        for m in messages:
            tokens += tokenize(m)

        top = [w for w, _ in Counter(tokens).most_common(6)]

        templates = [
            "Limited time: {benefit}. Shop now — {cta}!",
            "Discover {benefit} that fits you. {cta}",
            "Feel confident with {product}. {cta}",
            "{product} — comfort meets style. {cta}",
            "New drop: {benefit}. Tap to shop!",
            "Don't miss out — {benefit}. {cta}",
        ]

        ctas = ["Shop now", "Buy today", "Get yours", "See more", "Grab now"]

        suggestions = []
        benefit = ", ".join(top[:3]) if top else "premium comfort"
        product = " ".join(top[:2]) if top else "our best seller"

        for i, t in enumerate(templates[:n]):
            suggestion = t.format(
                benefit=benefit,
                product=product,
                cta=ctas[i % len(ctas)],
            )

            suggestions.append({
                "variant_id": str(uuid.uuid4()),
                "suggestion": suggestion,
                "rationale": f"Using top keywords: {top[:3]}"
            })

        return suggestions
