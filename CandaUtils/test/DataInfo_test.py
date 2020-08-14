import unittest
import CandaUtils as cu

class Test_DataInfo(unittest.TestCase):
    def test_Init_E(self):
        h = cu.DataInfo()
        assert 0 == h

    def test_setNumber(self):
        h = cu.DataInfo()
        h.setNumber(4)
        assert 4 == h

    def test_BinTextOutput(self):
        h = cu.DataInfo(0,64,'b')
        h.setNumber(0b100)

        assert str(h) == '0000000000000000000000000000000000000000000000000000000000000100', '__str__ method not correct (bin)'
        assert h.getFormatted() == '0000000000000000000000000000000000000000000000000000000000000100',  'getFormatted method not correct (bin)'
        #digit counting             |64     |54     |48     |40     |32     |24     |16     |8      |0 

    def test_SetFormat(self):
        h = cu.DataInfo()
        start = 2
        size = 2
        style = 'i'
        pad = ''

        h.setFormat(start, size, style, pad)
        h.setNumber(0b11010)
        assert h.len() == 2,  'Lenmethod not correct'
        assert h.getNumber == 2, 'getNumber method not correct'
        assert str(h) == ' 2',  '__str__ formatting method not correct'

    def test_SetTextFormat(self):
        h = cu.DataInfo()
        fmtString = '2:2:0'

        h.setTextFormat(fmtString)
        h.setNumber(0b11010)
        assert h.len() == size,  'Lenmethod not correct'
        assert h.getNumber == 2, 'getNumber method not correct'
        assert str(h) == '02',  '__str__ formatting method not correct (int)'
        assert h.getFormatted() == '2',  'getFormatted formatting method not correct (int)'

    def test_SetTextFormat(self):
        h = cu.DataInfo()
        fmtString = '2:4:0x'

        h.setTextFormat(fmtString)
        h.setNumber(0b111100)
        assert h.len() == 4,  'Lenmethod not correct'
        assert h.getNumber == 0xf, 'getNumber method not correct'
        assert str(h) == '0f',  '__str__ formatting method not correct (hex)'
        assert h.getFormatted() == 'f',  'getFormatted formatting method not correct (hex)'

    

    def test_setID():
        h = cu.DataInfo()
        assert h._id == 0, '__init__ method id assignment failed'
        h.setID(4000)
        assert h._id == 4000, 'setID method id assignment failed'

    def test_P(self):
        h = cu.DataInfo()
        assert 1 == h + 1,  'Test plus failed'

    def test_M(self):
        h = cu.DataInfo()
        assert -1 == h - 1, 'Test minus failed'

    def test_GE(self):
        h = cu.DataInfo()
        assert 1 >= h,      'Test >= failed'

    def test_LE(self):
        h = cu.DataInfo()
        assert  -1 <= h,    'Test <= failed'

    def test_EG(self):
        h = cu.DataInfo()
        assert 1 > h,      'Test >= failed'

    def test_EL(self):
        h = cu.DataInfo()
        assert -1 < h,      'Test <= failed'

    def test_NE(self):
        h = cu.DataInfo()
        assert -1 != h,     'Test != failed'

    def test_T(self):
        h = cu.DataInfo()
        h.setNumber(2)
        assert 4 == h * 2,  'Test times failes'

    def test_DReverse(self):
        h = cu.DataInfo()
        h.setNumber(2)
        assert 0.5 == 1 / h,'Test devide failed'

    def test_D(self):
        h = cu.DataInfo()
        h.setNumber(6)
        assert 3 == h / 2,  'Test devide failed'

    def test_IDReverse(self):
        h = cu.DataInfo()
        h.setNumber(2)
        assert 1 == 2.5 // h,'Test int devide failed'

    def test_TReverse(self):
        h = cu.DataInfo()
        h.setNumber(2)
        assert 20 == 10 * h,     'Test times failes'

    def test_ID(self):
        h = cu.DataInfo()
        h.setNumber(32)
        assert 13.0 == h // 2.4,'Test int devide failed'



if __name__ == '__main__':
    unittest.main()
