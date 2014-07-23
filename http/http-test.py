import http

from   textwrap import dedent
import unittest
from   unittest import TestCase


class TestHeader(TestCase):

    def test_parse(self):
        header = http._parse_header([
            'Header1: foo',
            'Header2: bar',
            'A-nice-header: pretty nice!',
            ])
        self.assertEqual(len(header), 3)
        self.assertEqual(header['Header1'], 'foo')
        self.assertEqual(header['Header2'], 'bar')
        self.assertEqual(header['A-nice-header'], 'pretty nice!')
        

    def test_parse_tricky(self):
        header = http._parse_header([
            'Header1: foo  ',
            'Header2:   ::bar::',
            'A-nicé-header: ¡Pretty nice!',
            ])
        self.assertEqual(len(header), 3)
        self.assertEqual(header['Header1'], 'foo')
        self.assertEqual(header['Header2'], '::bar::')
        self.assertEqual(header['A-nicé-header'], '¡Pretty nice!')
        


if __name__ == '__main__':
    unittest.main()

