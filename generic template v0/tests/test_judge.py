from core.judge import judge

def test_runs():
    res = judge(
        question="Is there quantum advantage?", 
        answer="We show exponential speedup on general ML.",
        context_docs=["Some context."],
        rubric_path="domains/default/domain_rules/example_rubric.yaml")
    assert "score" in res and "details" in res
