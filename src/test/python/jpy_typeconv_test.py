import unittest
import jpy
import numpy as np
import array

debug = True
debug = False
jpy.create_jvm(options=['-Djava.class.path=target/test-classes', '-Xmx512M'], debug=debug)


class TestTypeConversions(unittest.TestCase):


    def setUp(self):
        self.Fixture = jpy.get_class('org.jpy.fixtures.TypeConversionTestFixture')
        self.assertTrue('org.jpy.fixtures.TypeConversionTestFixture' in jpy.types)


    def test_ToObjectConversion(self):
        fixture = self.Fixture()
        self.assertEqual(fixture.stringifyObjectArg(12), 'Integer(12)')
        self.assertEqual(fixture.stringifyObjectArg(0.34), 'Double(0.34)')
        self.assertEqual(fixture.stringifyObjectArg('abc'), 'String(abc)')

        with self.assertRaises(ValueError) as e:
            fixture.stringifyObjectArg(1 + 2j)
        self.assertEqual(str(e.exception), 'cannot convert a Python complex to a Java java.lang.Object')


    def test_ToPrimitiveArrayConversion(self):
        fixture = self.Fixture()

        # Python int array to Java int array
        a = array.array('i', [1,2,3])
        self.assertEqual(fixture.stringifyIntArrayArg(a), 'int[](1,2,3)')

        # numpy int array to Java int array
        a = np.array([1,2,3], dtype=np.int32)
        self.assertEqual(fixture.stringifyIntArrayArg(a), 'int[](1,2,3)')

        a = [1, 2, 3]
        # list to Java int array - todo
        #self.assertEqual(fixture.stringifyIntArrayArg(a), 'int[](1,2,3)')

        a = (1, 2, 3)
        # tuple to Java int array - todo
        #self.assertEqual(fixture.stringifyIntArrayArg(a), 'int[](1,2,3)')

        with self.assertRaises(RuntimeError) as e:
            fixture.stringifyIntArrayArg(1 + 2j)
        self.assertEqual(str(e.exception), 'no matching Java method overloads found')


    def test_ToObjectArrayConversion(self):
        fixture = self.Fixture()

        self.assertEqual(fixture.stringifyObjectArrayArg(('A', 12, 3.4)), 'Object[](String(A),Integer(12),Double(3.4))')
        self.assertEqual(fixture.stringifyObjectArrayArg(['A', 12, 3.4]), 'Object[](String(A),Integer(12),Double(3.4))')
        #self.assertEqual(fixture.stringifyObjectArrayArg(['A', (1, 2, 3), 'C']), 'grrr!')

        self.assertEqual(fixture.stringifyStringArrayArg(('A', 'B', 'C')), 'String[](String(A),String(B),String(C))')
        self.assertEqual(fixture.stringifyStringArrayArg(['A', 'B', 'C']), 'String[](String(A),String(B),String(C))')


if __name__ == '__main__':
    print('\nRunning', __file__)
    unittest.main()
