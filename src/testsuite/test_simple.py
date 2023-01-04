#!/usr/bin/python3
import unittest
from common import dataformat

class TestSimple(unittest.TestCase):
    def setUp(self):
        return super().setUp()
    
    def  tearDown(self):
        return super().tearDown()

    def TestDecimals(self):
        print(dataformat.ToWei("1",0))
        print(dataformat.ToWei("1",1))
        print(dataformat.ToWei("1",6))
        print(dataformat.ToWei("1",18))
        
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

