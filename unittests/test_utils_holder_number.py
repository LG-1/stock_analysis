from ..utils.holder_number import HolderNumber



def test_holder_number():
    hn = HolderNumber()
    table = hn.get_holder_number_table('sz000008')
    assert table.shape[1] in [0, 11]
