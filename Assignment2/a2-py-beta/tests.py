from erd import *
from table import *
from erd_converter import convert_to_table

import unittest

# Check that the `__eq__` function works correctly on the sample table
class TestEquality(unittest.TestCase):
	def test_equal_db(self):
		sample_db2 = Database([ \
			Table('A', set(['a1','a2']), set(['a1']), set()), \
			Table('B', set(['b1','b2']), set(['b1']), set()), \
			Table('R1', set(['a1','b1','x']), set(['a1','b1']), \
				set([(('a1',), 'A', ('a1',)), (('b1',), 'B', ('b1',))]))])
		self.assertEqual( sample_db, sample_db2 )


# Check that the `convert_to_table()` function converts the sample_erd into the sample_db
class TestSample(unittest.TestCase):
	def test_converter(self):
		self.assertEqual( sample_db1, convert_to_table( sample_erd1 ))

	def test_converter2(self):
		self.assertEqual( sample_db2, convert_to_table( sample_erd2 ))

	def test_converter3(self):
		self.assertEqual( sample_db3, convert_to_table( sample_erd3 ))

	def test_converter4(self):
		self.assertEqual( sample_db4, convert_to_table( sample_erd4 ))

	def test_converter5(self):
		self.assertEqual( sample_db5, convert_to_table( sample_erd5 ))

	def test_converter6(self):
		self.assertEqual( sample_db6, convert_to_table( sample_erd6 ))

	def test_converter7(self):
		self.assertEqual( sample_db7, convert_to_table( sample_erd7 ))

	def test_converter8(self):
		self.assertEqual( sample_db8, convert_to_table( sample_erd8 ))

	def test_converter9(self):
		self.assertEqual( sample_db9, convert_to_table( sample_erd9 ))

	def test_converter_10(self):
		self.assertEqual( sample_db10, convert_to_table( sample_erd10 ))

	def test_converter_21(self):
		self.assertEqual( sample_db21, convert_to_table( sample_erd21 ))

# Run all unit tests above.
unittest.main(argv=[''],verbosity=2, exit=False)
