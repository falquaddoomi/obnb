from common import *
from NLEval.util.IDmap import IDmap
from NLEval.util import checkers

class TestIDmap(unittest.TestCase):
	def setUp(self):
		self.IDmap = IDmap()
		self.IDmap.addID('a')

	def tearDown(self):
		self.IDmap = None

	def test_size(self):
		self.assertEqual(self.IDmap.size, 1)
		self.IDmap.addID('b')
		self.assertEqual(self.IDmap.size, 2)

	def test_data(self):
		self.assertEqual(self.IDmap.data, {'a':0})
		self.IDmap.addID('b')
		self.assertEqual(self.IDmap.data, {'a':0,'b':1})

	def test_lst(self):
		self.assertEqual(self.IDmap.lst, ['a'])
		self.IDmap.addID('b')
		self.assertEqual(self.IDmap.lst, ['a','b'])

	def test_newID(self):
		self.assertRaises(AssertionError, self.IDmap.addID, 'a')

	def test_getitem(self):
		self.assertEqual(self.IDmap['a'], 0)

	def test_idx2ID(self):
		self.assertEqual(self.IDmap.idx2ID(0), 'a')

	def test_IDary2idxary(self):
		self.IDmap.addID('b')
		self.assertEqual(self.IDmap[['b','a']][0], 1)
		self.assertEqual(self.IDmap[['b','a']][1], 0)
		self.assertEqual(self.IDmap[np.array(['a','b'])][0], 0)
		self.assertEqual(self.IDmap[np.array(['a','b'])][1], 1)

	def test_contains(self):
		self.assertTrue('a' in self.IDmap)
		self.assertFalse('b' in self.IDmap)
		self.IDmap.addID('b')
		self.assertTrue('b' in self.IDmap)

	def test_eq(self):
		self.IDmap.addID('b')
		idmap = IDmap()
		idmap.addID('b')
		idmap.addID('a')
		self.assertTrue(self.IDmap == idmap)
		self.IDmap.addID('c')
		self.IDmap.addID('d')
		idmap.addID('d')
		self.assertFalse(self.IDmap == idmap)
		idmap.addID('c')
		self.assertTrue(self.IDmap == idmap)

	def test_iter(self):
		self.IDmap.addID('b')
		self.IDmap.addID('x')
		lst = ['a', 'b', 'x']
		for i, j in enumerate(self.IDmap):
			with self.subTest(i=i):
				self.assertEqual(j, lst[i])

class TestCheckers(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		n = 10
		self.n = n
		self.n_str = str(n)
		self.n_int = int(n)
		self.n_npint = np.int(n)
		self.n_npint64 = np.int64(n)
		self.n_float = float(n)
		self.n_npfloat = np.float(n)
		self.n_npfloat128 = np.float128(n)
		self.n_int_tuple = (int(n), int(n), int(n))
		self.n_int_lst = [int(n), int(n), int(n)]
		self.n_int_npary = np.array([n, n, n], dtype=int)
		self.n_float_tuple = (float(n), float(n), float(n))
		self.n_float_lst = [float(n), float(n), float(n)]
		self.n_float_npary = np.array([n, n, n], dtype=float)

	def test_INT_TYPE(self):
		self.assertIsInstance(self.n_int, checkers.INT_TYPE)
		self.assertIsInstance(self.n_npint, checkers.INT_TYPE)
		self.assertIsInstance(self.n_npint64, checkers.INT_TYPE)
		self.assertNotIsInstance(self.n_float, checkers.INT_TYPE)
		self.assertNotIsInstance(self.n_npfloat, checkers.INT_TYPE)
		self.assertNotIsInstance(self.n_npfloat128, checkers.INT_TYPE)

	def test_FLOAT_TYPE(self):
		self.assertNotIsInstance(self.n_int, checkers.FLOAT_TYPE)
		self.assertNotIsInstance(self.n_npint, checkers.FLOAT_TYPE)
		self.assertNotIsInstance(self.n_npint64, checkers.FLOAT_TYPE)
		self.assertIsInstance(self.n_float, checkers.FLOAT_TYPE)
		self.assertIsInstance(self.n_npfloat, checkers.FLOAT_TYPE)
		self.assertIsInstance(self.n_npfloat128, checkers.FLOAT_TYPE)

	def test_ITERABLE_TYPE(self):
		n_int_tuple = (1, 2, 3)
		n_int_lst = [1, 2, 3]
		n_int_ary = np.array([1, 2, 3])
		self.assertIsInstance(n_int_tuple, checkers.ITERABLE_TYPE)
		self.assertIsInstance(n_int_lst, checkers.ITERABLE_TYPE)
		self.assertIsInstance(n_int_ary, checkers.ITERABLE_TYPE)

	def test_checkType(self):
		checkers.checkType('n_int', int, self.n_int)
		self.assertRaises(TypeError, checkers.checkType, 'n_int', int, self.n_float)
		checkers.checkType('n_float', float, self.n_float)
		self.assertRaises(TypeError, checkers.checkType, 'n_float', float, self.n_int)
		checkers.checkType('n_str', str, self.n_str)

	def test_checkTypeInIterable(self):
		checkers.checkTypesInIterable('n_int_tuple', checkers.INT_TYPE, self.n_int_tuple)
		checkers.checkTypesInIterable('n_int_lst', checkers.INT_TYPE, self.n_int_lst)
		checkers.checkTypesInIterable('n_int_npary', checkers.INT_TYPE, self.n_int_npary)
		self.assertRaises(TypeError, checkers.checkTypesInIterable, \
			'n_int_tuple', checkers.FLOAT_TYPE, self.n_int_tuple)
		self.assertRaises(TypeError, checkers.checkTypesInIterable, \
			'n_int_lst', checkers.FLOAT_TYPE, self.n_int_lst)
		self.assertRaises(TypeError, checkers.checkTypesInIterable, \
			'n_int_npary', checkers.FLOAT_TYPE, self.n_int_npary)
		checkers.checkTypesInIterable('n_float_tuple', checkers.FLOAT_TYPE, self.n_float_tuple)
		checkers.checkTypesInIterable('n_float_lst', checkers.FLOAT_TYPE, self.n_float_lst)
		checkers.checkTypesInIterable('n_float_npary', checkers.FLOAT_TYPE, self.n_float_npary)
		self.assertRaises(TypeError, checkers.checkTypesInIterable, \
			'n_float_tuple', checkers.INT_TYPE, self.n_float_tuple)
		self.assertRaises(TypeError, checkers.checkTypesInIterable, \
			'n_float_lst', checkers.INT_TYPE, self.n_float_lst)
		self.assertRaises(TypeError, checkers.checkTypesInIterable, \
			'n_float_npary', checkers.INT_TYPE, self.n_float_npary)

	def test_checkTypeErrNone(self):
		self.assertRaises(ValueError, checkers.checkTypeErrNone, 'n', int, None)
		self.assertRaises(ValueError, checkers.checkTypeErrNone, 'n', float, None)
		self.assertRaises(ValueError, checkers.checkTypeErrNone, 'n', str, None)

	def test_checkTypeAllowNone(self):
		checkers.checkTypeAllowNone('n', int, None)
		checkers.checkTypeAllowNone('n', float, None)
		checkers.checkTypeAllowNone('n', str, None)

	def test_checkNumpyArrayNDim(self):
		ary1 = np.ones(2)
		ary2 = np.ones((2,2))
		ary3 = np.ones((2,2,2))
		checkers.checkNumpyArrayNDim('ary1', 1, ary1)
		checkers.checkNumpyArrayNDim('ary2', 2, ary2)
		checkers.checkNumpyArrayNDim('ary3', 3, ary3)
		self.assertRaises(ValueError, checkers.checkNumpyArrayNDim, 'ary1', 4, ary1)
		self.assertRaises(ValueError, checkers.checkNumpyArrayNDim, 'ary2', 4, ary2)
		self.assertRaises(ValueError, checkers.checkNumpyArrayNDim, 'ary3', 4, ary3)

	def test_checkNumpyArrayShape(self):
		ary1 = np.ones(2)
		ary2 = np.ones((2,2))
		ary3 = np.ones((2,2,2))
		checkers.checkNumpyArrayShape('ary1', 2, ary1)
		checkers.checkNumpyArrayShape('ary1', (2,), ary1)
		checkers.checkNumpyArrayShape('ary2', (2, 2), ary2)
		checkers.checkNumpyArrayShape('ary3', (2, 2, 2), ary3)
		self.assertRaises(ValueError, checkers.checkNumpyArrayShape, 'ary1', 1, ary1)
		self.assertRaises(ValueError, checkers.checkNumpyArrayShape, 'ary1', (1, 2,), ary1)
		self.assertRaises(ValueError, checkers.checkNumpyArrayShape, 'ary2', (2, 1), ary2)
		self.assertRaises(ValueError, checkers.checkNumpyArrayShape, 'ary3', 1, ary3)

if __name__ == '__main__':
	unittest.main()
