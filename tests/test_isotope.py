import unittest
from ZapMeNot import isotope


class testIsotope(unittest.TestCase):
	# test response to a bad isotope name
	def test_a_bad_material_name(self):
		self.assertRaises(ValueError, isotope.Isotope, "wanker")

	# test valid half life in years
	def test_halflifeYears(self):
		a = isotope.Isotope("co-60")
		self.assertAlmostEqual(a.half_life, 5.271*365.25*24*60*60)

	# test valid half life in days

	# test valid half life in hours
	def test_halflifeMinutes(self):
		a = isotope.Isotope("cu-67")
		self.assertAlmostEqual(a.half_life, 61.86*60*60)

	# test valid half life in minutes
	def test_halflifeMinutes(self):
		a = isotope.Isotope("c-11")
		self.assertAlmostEqual(a.half_life, 20.38*60)

	# test valid half life in seconds

	# test valid photon property read and store
	def test_photon_readAndStore(self):
		a = isotope.Isotope("co-60")
		self.assertEqual(a.photons, [[3.46930e-01, 7.59999e-05], \
  									 [8.26280e-01, 7.59999e-05], \
  									 [1.17321e+00, 9.99000e-01], \
  									 [1.33247e+00, 9.99824e-01], \
  									 [2.15877e+00, 1.10000e-05], \
  									 [2.50500e+00, 3.60000e-08]])



