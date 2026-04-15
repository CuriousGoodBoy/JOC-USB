from analysis.health_scorer import score_health


def test_score_health_bounds():
    assert 0 <= score_health([]) <= 100
