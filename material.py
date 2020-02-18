import numpy as np
import yaml

class Material:
	library = None

	def __init__(self,name="void"):
		#initialize the class library if it has not already been done
		if Material.library is None:
			stream = open("materials.yml", 'r')
			Material.library = yaml.load(stream, Loader=yaml.FullLoader)
			stream.close()

		# check to see if the name is in the library
		if name not in Material.library.keys():
			raise ValueError("Material not found in the Material Library")

		# initialize the object
		self.name = name
		properties = Material.library.get(self.name)
		self.density = properties.get("density")
		self.energy_bins = np.array(properties.get("energy"))
		self.mass_atten_coff = np.array(properties.get("mass-atten-coff"))
		gp_array = properties.get("gp-coeff")
		self.gp_b = np.array(gp_array[:][0])
		self.gp_c = np.array(gp_array[:][1])
		self.gp_a = np.array(gp_array[:][2])
		self.gp_X = np.array(gp_array[:][3])
		self.gp_d = np.array(gp_array[:][4])

	def setDensity(self, density):
		self.density = density

	def getMfp(self, energy, distance):
		return distance * self.density / self.getMassAttenCoff(energy)

	def getMassAttenCoff(self, energy):
		if (energy < self.energy_bins[0]) or (energy > self.energy_bins[-1]):
			raise ValueError("Photon energy is out of range")
		return np.interp(energy, self.energy_bins, self.mass_atten_coff)

	def getBuildupFactor(self, energy, mfp, type="GP"):
		if type == "GP":
			# find the bounding array indices
			if (energy < self.energy_bins[0]) or (energy > self.energy_bins[-1]):
				raise ValueError("Photon energy is out of range")
			b = np.interp(energy, self.energy_bins, gp_b)
			c = np.interp(energy, self.energy_bins, gp_c)
			a = np.interp(energy, self.energy_bins, gp_a)
			X = np.interp(energy, self.energy_bins, gp_X)
			d = np.interp(energy, self.energy_bins, gp_d)
			return self.GP(a,b,c,d,X,mfp)
		else:
			raise ValueError("Only GP Buildup Factors are currently supported")

	def GP(self, a, b, c, d, X, mfp):
		K = (c * (mfp**a)) + (d * (np.tanh(mfp/X -2) - np.tanh(-2))) / (1 - np.tanh(-2))
		#print(K)
		if K == 1:
			return 1 + (b-1) * mfp
		else:
			return 1 + (b-1)*((K**mfp) - 1)/(K -1)
	


