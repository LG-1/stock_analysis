from ..utils.stock_markets import number_dot_upper2lower_number, lower_number2number_dot_upper


def test_case1():
    assert number_dot_upper2lower_number("000001.SZ") == "sz000001"

def test_case2():
    assert lower_number2number_dot_upper(number_dot_upper2lower_number("000001.SZ")) == "000001.SZ"