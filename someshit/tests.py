import unittest
from code import series_sum

class TT(unittest.TestCase):
    """SERIES TEST'S"""
    def test_mixed_numb(self):

        call = series_sum([1,2.5,3,4])
        result = '12.534'
        self.assertEqual(
            call, result, 'Со списком у series_sum() have troubles'
        )
    def test_mixed_numb_strings(self):
        call = series_sum([1, 'fff', 3, 4])
        result = '1fff34'
        self.assertEqual(
            call, result, 'PIZDEC smeshat ne poluchilos`'
        )
    def test_empty(self):
        call = series_sum([])
        result = 'ff'
        self.assertEqual(
            call, result, 'eblany'
        )
    
if __name__ == '__main__':
    unittest.main()