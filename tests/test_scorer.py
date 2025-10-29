from core.scorer import score_candidate

def test_score_candidate():
    score = score_candidate(['Python','SQL'], 5)
    assert isinstance(score, int)
    assert 0 <= score <= 100
