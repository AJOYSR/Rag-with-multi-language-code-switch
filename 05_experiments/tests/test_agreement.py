from src.agreement import cohen_kappa


def test_kappa_known_value():
    a = [1, 1, 0, 0, 1, 0, 1, 1]
    b = [1, 0, 0, 0, 1, 1, 1, 1]
    po, k = cohen_kappa(a, b)
    assert po == 0.75
    assert abs(k - (0.75 - 0.53125) / (1 - 0.53125)) < 1e-12


def test_kappa_undefined_single_category():
    assert cohen_kappa([True] * 5, [True] * 5) == (1.0, None)
