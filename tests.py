# 
#   Create tests for functions/classes in firmware.py
#   Run this file with "pytest tests.py -v"
#
import unittest
import firmware

class FirmwareTest(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def test_add_integers(self):
        self.assertEqual(5 + 5, 10)

    def test_add_negative(self):
        self.assertEqual(-5 + 5, 0)

