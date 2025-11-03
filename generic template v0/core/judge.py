from typing import List, Dict, Any
import os, yaml
from core.rubric_schema import Rubric
from configs.settings import settings

# Optional LLM support (OpenAI). If not present, fall back to lexical checks.
_openai = None
try:
    from openai import OpenAI
    if settings.openai_api_key:
        _openai = OpenAI(api_key=settings.openai_api_key)
except Exception:
    _openai = None

def _lexical_check(rule, text: str) -> bool:
        params = rule.params or {}
        tokens = [t.lower() for t in params.get("terms", [])]
        t = text.lower()
        if rule.checker == "contains_any":
            return any(tok in t for tok in tokens)
        if rule.checker == "contains_all":
            return all(tok in t for tok in tokens)
        return False

def _llm_check(rule, question: str, answer: str, context: str) -> bool:
        if not _openai:
            # Without LLM, assume uncertain => 0.5 pass to avoid harsh false negatives
            return False
        prompt = f"""You are a rigorous evaluator.
        Rule: {rule.description}
        Question: {question}
        Answer: {answer}
        Context:
{context}

        Respond ONLY with PASS or FAIL based on the rule."""
        try:
            resp = _openai.chat.completions.create(
                model=settings.openai_model,
                messages=[{"role":"user","content":prompt}],
                temperature=0.0,
            )
            content = resp.choices[0].message.content.strip().upper()
            return content.startswith("PASS")
        except Exception:
            return False

def judge(question: str, answer: str, context_docs: List[str], rubric_path: str) -> Dict[str, Any]:
        with open(rubric_path, "r", encoding="utf-8") as f:
            rub = Rubric.model_validate(yaml.safe_load(f))

        total_weight = sum(r.weight for r in rub.rules) or 1.0
        earned = 0.0
        details = []
        context_concat = "\n\n".join(context_docs or [])

        for r in rub.rules:
            if r.checker in ("contains_any", "contains_all"):
                ok = _lexical_check(r, answer + "\n" + context_concat)
            else:
                ok = _llm_check(r, question, answer, context_concat)

            score = r.weight if ok else 0.0
            earned += score
            details.append({
                "rule_id": r.id,
                "description": r.description,
                "passed": bool(ok),
                "weight": r.weight,
                "severity": r.severity
            })

        final = earned / total_weight
        return {
            "score": round(final, 3),
            "passed": final >= rub.passing_score,
            "details": details,
            "rubric": {"name": rub.name, "version": rub.version, "passing_score": rub.passing_score}
        }
