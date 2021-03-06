
import csv
import collections
import numpy
import itertools
from copy import copy

def makeKeyorder(maxstrandlen,motiflist): # create the keyorder for the order of our dictionary
	
	keyorder = []
	elongkeyorder = []

	for n in range(maxstrandlen): 
		for key in itertools.product(range(2),repeat = n+1):
			mod_key = str(key).strip(" ,(),','").replace(", ", "")
			if len(keyorder) > 0:
				if len(mod_key) == len(keyorder[-1]):
					has_placed = False
					for keys_so_far in range(len(keyorder)):
						if len(mod_key) == len(keyorder[keys_so_far]):
							if mod_key.count('1') < keyorder[keys_so_far].count('1') and has_placed == False:
								keyorder.insert(keys_so_far,mod_key)
								has_placed = True
								break
					if has_placed == False:
						keyorder.append(mod_key)
				else:
					keyorder.append(mod_key)
			else:
				keyorder.append(mod_key)

		for key in itertools.product(range(len(motiflist)+1),repeat = n+1):
			mod_key = str(key).strip(" ,(),','").replace(", ", "").replace(str(len(motiflist)),"-")
			if len(elongkeyorder) > 0:
				if len(mod_key) == len(elongkeyorder[-1]):
					has_placed = False
					for keys_so_far in range(len(elongkeyorder)):
						if len(mod_key) == len(elongkeyorder[keys_so_far]):
							if mod_key.count('1') < elongkeyorder[keys_so_far].count('1') and mod_key.count('-') < elongkeyorder[keys_so_far].count('-'):
								elongkeyorder.insert(keys_so_far,mod_key)
								break
					else:
						elongkeyorder.append(mod_key)
				else:
					elongkeyorder.append(mod_key)
			else:
				elongkeyorder.append(mod_key)

	return keyorder, elongkeyorder

def motifcompetesim_elongdataoutput(parameterlist,masterprefix,testprefix,pop_tracker,nr_strands_per_time,elongation_tracker,strand_number_dict,trials,max_strand_nr,maxStrandLength,numCells,numRounds,motiflist,elong,biaslist):

	keyorder, elongkeyorder = makeKeyorder(maxStrandLength,motiflist)

	dict_per_time = []
	for time_point in xrange(numRounds):
		temp2_dict = {}
		for key in keyorder:
			temp2_dict[key] = {}
			for elongkey in elongkeyorder:
				temp2_dict[key][elongkey] = [0 for trial in xrange(trials)]
			temp2_dict[key] = collections.OrderedDict(sorted(temp2_dict[key].items(), key = lambda i:elongkeyorder.index(i[0])))
		dict_per_time.append(collections.OrderedDict(sorted(temp2_dict.items(), key = lambda i:keyorder.index(i[0]))))

		for trial in xrange(trials):
			for cell in xrange(len(pop_tracker[trial][time_point])):
				for strand in xrange(len(pop_tracker[trial][time_point][cell])):
					dict_per_time[time_point][pop_tracker[trial][time_point][cell][strand]][elongation_tracker[trial][time_point][cell][strand]][trial] += 1
			for key in keyorder:
				for elongkey in elongkeyorder:
					if float(strand_number_dict[trial][time_point][key]) > 0:
						dict_per_time[time_point][key][elongkey][trial] = int(dict_per_time[time_point][key][elongkey][trial])/float(strand_number_dict[trial][time_point][key])
					else:
						dict_per_time[time_point][key][elongkey][trial] = int(dict_per_time[time_point][key][elongkey][trial])


	with open(masterprefix + testprefix +'_ElongData_motif{motif}_len{maxStrandLength}_bias{bias}_elong{elong}_{trials}trials_numRound{numRounds}.csv'.format(motif =  '|'.join([repr(motif) for motif in motiflist]), maxStrandLength = maxStrandLength, bias= '|'.join([str(bias) for bias in biaslist]), elong=elong, trials=trials, numRounds=numRounds), 'wb') as f:
		parameter_writer = csv.writer(f)
		strand_writer = csv.writer(f, quotechar="'", quoting=csv.QUOTE_ALL)

		parameter_writer.writerow(parameterlist)
		strand_writer.writerow(elongkeyorder)
		strand_writer.writerow(keyorder)

		for time_point in xrange(numRounds):
			for elongkey in elongkeyorder:
				time_elong_list = []
				for key in keyorder:
					time_elong_list.append(numpy.mean(dict_per_time[time_point][key][elongkey]))
				parameter_writer.writerow(time_elong_list)
		for time_point in xrange(numRounds):
			for elongkey in elongkeyorder:
				time_elong_list = []
				for key in keyorder:
					time_elong_list.append(numpy.std(dict_per_time[time_point][key][elongkey],dtype=numpy.float64))
				parameter_writer.writerow(time_elong_list)

	f.close()