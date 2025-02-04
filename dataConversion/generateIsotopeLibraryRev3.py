# program to generate Rev 2 of isotopeLibrary.yml
import yaml

def float_representer(dumper, value):
    text = '{0:.5e}'.format(value)
    return dumper.represent_scalar(u'tag:yaml.org,2002:float', text)
yaml.add_representer(float, float_representer)

# open and read the decay data
stream = open("origen.rev03.decay.data", 'r')
isotopeLibrary = {}
while True:
	data = stream.readline() #read the title card and throw it away
	if not data:
		break
	while True:
		currentIsotope = {}
		# read data until we run out
		data = stream.readline()
		tokens = data.split()
		if tokens[0] == "-1":
			break
		stream.readline()
		stream.readline()
		nuclide = tokens[1]
		halflifeUnits = int(tokens[2])
		halflife = float(tokens[3])
		if halflifeUnits == 1:
			halflifeUnits = "second"
		elif halflifeUnits == 2:
			halflifeUnits = "minute"
		elif halflifeUnits == 3:
			halflifeUnits = "hour"
		elif halflifeUnits == 4:
			halflifeUnits = "day"
		elif halflifeUnits == 5:
			halflifeUnits = "year"
		elif halflifeUnits == 6:
			halflifeUnits = "stable"
		elif halflifeUnits == 7:
			halflifeUnits = "year"
			halflife = halflife * 1E3
		elif halflifeUnits == 8:
			halflifeUnits = "year"
			halflife = halflife * 1E6
		elif halflifeUnits == 9:
			halflifeUnits = "year"
			halflife = halflife * 1E9
		else:
			raise ValueError("Unknown halflife units")
		# build the dictionary entry for the current isotope
		currentIsotope.update({"half-life" : halflife})
		currentIsotope.update({"half-life-units" : halflifeUnits})
		# add the current isotope to the library dictionary
		isotopeLibrary.update({nuclide : currentIsotope})
stream.close()

# -------------------------------------------------------------
# open and read the photon data
stream = open("origen.rev04.mpdkxgam.data", 'r')
finalLibrary = {}
while True:
	# read data until we run out
	data = stream.readline()
	if not data:
		break
	tokens = data.split()
	nuclide = tokens[0]
	nuclide_int = int(nuclide)
	# create an isotope name in the form of "Np-237m"
	abbreviation = tokens[6].capitalize()
	Z = nuclide_int//10000  # atomic number
	A = (nuclide_int-(Z*10000))//10  # atomic mass number
	I = int(nuclide_int) - (Z*10000 + A*10) # metastable state
	if I > 0:
		metastable_state = chr(108+I)
	else:
		metastable_state = ""
	name = abbreviation + "-" + str(A) + metastable_state
	# now we read enough lines to capture all of the photons, 6 per line
	photon_count = tokens[1]
	photon_count = int(photon_count.rstrip(photon_count[-1]))
	number_read = 0
	print(name + ": " + str(photon_count) + " photons")
	photonIntensities = []
	while True:
		data = stream.readline()
		tokens = data.split()
		photons_per_line = len(tokens)//2  # two tokens for each 
		for x in range(photons_per_line):
			photon_energy = tokens[0]
			photon_intensity = tokens[1]
			# check for valid photon energy
			if float(photon_energy) >15:  # flag photons > 15 MeV
				print("Skipping nuclide "+nuclide + ": photon energy = "+ photon_energy +", intensity = " + photon_intensity)
				#raise ValueError("Photon energy above 15 MeV")
			if float(photon_energy) > 15.01e-3: # limit photons to > 15.01 keV
				photonIntensities.append([float(photon_energy),float(photon_intensity)])
			else:
				print("dropping photon with energy = " + photon_energy + " MeV")
			del(tokens[0])
			del(tokens[0])
		number_read = number_read + photons_per_line
		if (number_read == photon_count):
			break
	if len(photonIntensities) == 0:
		print("Zero photons remaining for this isotope")
		
	# build the dictionary entry for the current isotope
	currentIsotope = isotopeLibrary[nuclide]
	# discard anything that is "observationaly stable" with some photon emission
	if currentIsotope["half-life-units"] != "stable":
		currentIsotope.update({"photon-energy-units" : "MeV"})
		currentIsotope.update({"photon-intensity" : photonIntensities})
		# "key_products" is a placeholder that will be filled in later
		currentIsotope.update({"key_progeny" : None})
		# add the current isotope to the library dictionary
		finalLibrary.update({name : currentIsotope})

# add two key isotopes that emit no photons but have daughters that may be important
name = "Sr-90"
nuclide = "380900"
currentIsotope = isotopeLibrary[nuclide]
currentIsotope.update({"photon-energy-units" : "MeV"})
currentIsotope.update({"photon-intensity" : None})
currentIsotope.update({"key_progeny" : None})
finalLibrary.update({name : currentIsotope})
name = "Ru-106"
nuclide = "441060"
currentIsotope = isotopeLibrary[nuclide]
currentIsotope.update({"photon-energy-units" : "MeV"})
currentIsotope.update({"photon-intensity" : None})
currentIsotope.update({"key_progeny" : None})
finalLibrary.update({name : currentIsotope})

# The following is a list of parent isotopes and products for select
# isotopes.  These are cases where a source will frequently list the
# parent isotope and assume the products are included.  The data here
# provides the equilibrium relative concentration of the products.
# The data was taken from the JANIS database of ENDF/B-VIII.0 data
# see https://www.oecd-nea.org/janisweb/tree/RDD/'ENDF/B-VIII.0'/RDD
parents_progeny = {"Ba-140":{"La-140":1.15157373}, 
			"Cs-137":{"Ba-137m":0.9469945}, 
			"Ce-144":{"Pr-144":0.99999331654,"Pr-144m":0.095478},
			"Ru-106":{"Rh-106":1.0},
			"Sr-90" :{"Y-90":1.0}, 
			"Sn-113":{"In-113m":1.0}, 
			"Ru-103":{"Rh-103m":0.988259}}
			
for key in parents_progeny:
	if key in finalLibrary.keys():
		data_to_be_modified = finalLibrary.get(key)
		progeny_to_add = parents_progeny.get(key)
		data_to_be_modified.update({"key_progeny" : progeny_to_add})
		finalLibrary.update({key : data_to_be_modified})

# write out the yaml library		
yamlStream = open('isotopeLibraryRev3.yml', 'wt')
yaml.dump(finalLibrary, yamlStream, default_flow_style=False, explicit_start=True, explicit_end=True)
stream.close()
yamlStream.close()
	
		

	
