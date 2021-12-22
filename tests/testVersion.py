import unittest

from src.semver import *


class TestInit(unittest.TestCase):
    def test_valid(self):
        Version(1, 0, 0)
        Version(1, 2, 0)
        Version(1, 2, 3)
        Version(1, 2, 3, 'pre1')

    def test_negativeMajor(self):
        with self.assertRaises(ValueError) as ve:
            Version(-1, 0, 0)

        self.assertEqual(str(ve.exception), 'Major value `-1` is invalid')

    def test_negativeMinor(self):
        with self.assertRaises(ValueError) as ve:
            Version(0, -1, 0)

        self.assertEqual(str(ve.exception), 'Minor value `-1` is invalid')

    def test_negativePatch(self):
        with self.assertRaises(ValueError) as ve:
            Version(0, 0, -1)

        self.assertEqual(str(ve.exception), 'Patch value `-1` is invalid')

    def test_emptyTag(self):
        with self.assertRaises(ValueError) as ve:
            Version(1, 0, 0, '')

        self.assertEqual(str(ve.exception), 'Empty tag value is invalid')

    def test_zeroVersion(self):
        with self.assertRaises(ValueError) as ve:
            Version(0, 0, 0)

        self.assertEqual(str(ve.exception), 'v0.0.0 is invalid')


class TestEqualityAndOrdering(unittest.TestCase):
    def test_equality(self):
        v0 = Version(1, 3, 4, 'pre2')
        v1 = Version(1, 3, 4, 'pre2')

        self.assertEqual(v0, v1)

    def test_ordering(self):
        v0 = Version(0, 1, 3)
        v1 = Version(1, 1, 3)
        v2 = Version(0, 1, 2)
        v3 = Version(2, 7, 1)
        v4 = Version(2, 7, 1)

        self.assertLess(v0, v1)
        self.assertLess(v2, v3)
        self.assertLess(v1, v3)
        self.assertLess(v2, v1)

        self.assertLessEqual(v3, v4)

        self.assertGreater(v1, v0)
        self.assertGreater(v3, v2)
        self.assertGreater(v3, v1)
        self.assertGreater(v1, v2)

        self.assertGreaterEqual(v3, v4)

        versions = [v0, v1, v2, v3]

        versions.sort()

        self.assertEqual(versions[0], v2)
        self.assertEqual(versions[1], v0)
        self.assertEqual(versions[2], v1)
        self.assertEqual(versions[3], v3)

    def test_wrongTypeOrdering(self):
        v = Version(1, 0, 0)
        
        with self.assertRaises(TypeError) as te:
            result = v < 0
        
        self.assertEqual(str(te.exception), 'Other argument is not a version')

        with self.assertRaises(TypeError) as te:
            result = v <= 0

        self.assertEqual(str(te.exception), 'Other argument is not a version')

        with self.assertRaises(TypeError) as te:
            result = v > 0

        self.assertEqual(str(te.exception), 'Other argument is not a version')

        with self.assertRaises(TypeError) as te:
            result = v >= 0

        self.assertEqual(str(te.exception), 'Other argument is not a version')


class TestStringAndParsing(unittest.TestCase):
    def test_string(self):
        v0 = Version(1, 12, 2, 'pre')

        self.assertEqual(v0.string, '1.12.2-pre')
        self.assertEqual(repr(v0), '1.12.2-pre')
        self.assertEqual(str(v0), 'v1.12.2-pre')

        v1 = Version(1, 12, 2)

        self.assertEqual(v1.string, '1.12.2')
        self.assertEqual(repr(v1), '1.12.2')
        self.assertEqual(str(v1), 'v1.12.2')

    def test_parse(self):
        v0 = Version(1, 12, 2, 'pre')

        self.assertEqual(Version.parse('1.12.2-pre'), v0)
        self.assertEqual(Version.parse('v1.12.2-pre'), v0)

        v1 = Version(1, 12, 2)

        self.assertEqual(Version.parse('1.12.2'), v1)
        self.assertEqual(Version.parse('v1.12.2'), v1)

        with self.assertRaises(ValueError) as ve:
            Version.parse('1.12')

        self.assertEqual(str(ve.exception), 'Invalid version "1.12"')

        with self.assertRaises(ValueError) as ve:
            Version.parse('1.12.2.oops')

        self.assertEqual(str(ve.exception), 'Invalid version "1.12.2.oops"')

        with self.assertRaises(ValueError) as ve:
            Version.parse('0.0.0.oops')

        self.assertEqual(str(ve.exception), 'Invalid version "0.0.0.oops"')

        with self.assertRaises(ValueError) as ve:
            Version.parse('0.0.0')

        self.assertEqual(str(ve.exception), '"0.0.0" is invalid')


if __name__ == '__main__':
    unittest.main()
