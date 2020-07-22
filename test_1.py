import unittest
import UI as u

class Test_DataInfo(unittest.TestCase):
    def test_Init_E(self):
        h = u.DataInfo()
        assert 0 == h

    def test_Set(self):
        h = u.DataInfo()
        h.set(4)
        assert 4 == h

    def test_SetFormat(self):
        h = u.DataInfo()
        start = 2
        size = 2
        type = 'd'
        formating = '~r'

        h.setFormat(start,size,type,formating)
        h.set(0b11010)
        assert len(h) == size,  "Length not correct"
        assert h._rawData == 2, "rawData not correct"
        assert str(h) == "02",  "__str__ not correct"

    def test_P(self):
        h = u.DataInfo()
        assert 1 == h + 1,  'Test plus failed'

    def test_M(self):
        h = u.DataInfo()
        assert -1 == h - 1, 'Test minus failed'

    def test_GE(self):
        h = u.DataInfo()
        assert 1 >= h,      'Test >= failed'

    def test_LE(self):
        h = u.DataInfo()
        assert  -1 <= h,    'Test <= failed'

    def test_EG(self):
        h = u.DataInfo()
        assert 1 > h,      'Test >= failed'

    def test_EL(self):
        h = u.DataInfo()
        assert -1 < h,      'Test <= failed'

    def test_NE(self):
        h = u.DataInfo()
        assert -1 != h,     'Test != failed'

    def test_T(self):
        h = u.DataInfo()
        h.set(2)
        assert 4 == h * 2,  'Test times failes'

    def test_DReverse(self):
        h = u.DataInfo()
        h.set(2)
        assert 0.5 == 1 / h,  'Test devide failed'

    def test_D(self):
        h = u.DataInfo()
        h.set(6)
        assert 3 == h / 2,  'Test devide failed'

    def test_IDReverse(self):
        h = u.DataInfo()
        h.set(2)
        assert 1 == 2.5 // h,'Test int devide failed'

    def test_TReverse(self):
        h = u.DataInfo()
        h.set(2)
        assert 20 == 10 * h,  'Test times failes'

    def test_ID(self):
        h = u.DataInfo()
        h.set(32)
        assert 13.0 == h // 2.4,'Test int devide failed'

    def test_ReverseBinary(self):
        h = u.DataInfo()
        start = 0
        size = 4
        type = 'b'
        formating = 'r'
        data = 0b11011

        h.setFormat(start,size,type,formating)
        h.set(data)
        assert len(h) == size,  "Length not correct"
        assert h._rawData == data, "rawData not correct"
        assert h == "1101",  "__str__ not correct"

    def test_HexTwos(self):
        h = u.DataInfo()
        start = 4
        size = 8
        type = 'x'
        formating = '2'
        data = 0b100010011011
        
        h.setFormat(start,size,type,formating)
        h.set(data)
        assert len(h) == size,  "Length not correct"
        assert h._rawData == data, "rawData not correct"
        assert h == "1101",  "__str__ not correct"




    


if __name__ == '__main__':
    unittest.main()
