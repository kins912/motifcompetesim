
import sys
import getopt
from motifcompetesim_motifoutput import motifcompetesim_motifoutput
from motifcompetesim_fulltrialoutput import motifcompetesim_fulltrialoutput
from motifcompetesim_allstrandoutput import motifcompetesim_allstrandoutput
from motifcompetesim_elongdataoutput import motifcompetesim_elongdataoutput

def usage():
	print "Running a Motif Simulation using the parameters designated by options\n"
	print "PARAMETERS:"
	print "--trials, --maxStrands, --maxStrandLength, --numCells, --numRounds, --motiflist, --elong, --biaslist, --elongdata\n"
	print "motiflist and biaslist must be the same length, where jth motif corresponds with the jth bias"
	print "Outputs three csv files:\n"
	print "1. 'MotifData' designates the csv file containing primarily motif data. First row is parameters."
	print "For each trial, a row of motif frequency per round, a row of freq of total nr_strands used per round, a row of freq_nr_cells_with_motif per round"
	print "Last 6 rows are mean (by round) of the three data types collected, and then standard deviation of the same.\n"
	print "2. 'FullTrial1Data' designates a csv file where each row represents the cell contents for a single cell at a particular time point (plus first row of parameters)."
	print "The first numCells rows are the cells after the first round.\n"
	print "3. 'AllStrandData' designates a csv file where the first row is a list of all possible strands in the simulation."
	print "The rows beneath correspond chronologically with time, first with all mean data and then with stdev data (mean1, mean2, ..., stdev1, stdev2, ...) "
	print "4. 'ElongData' designates a csv file where the first row is a list of the possible elongation patterns, the next row is the same as beginning of 'AllStrandData'"
	print "The rows beneath correspond chronologically with time and the elongationpattern, first with all mean data and then with stdev data (mean1-,mean1+,mean1--, ..., mean2-, ..., stdev1-,... stdev2-, ...) "

def main(argv):

	try:
		opts, args = getopt.getopt(argv, "h", ["help","testprefix=","trials=","maxStrands=","maxStrandLength=","numCells=","numRounds=","motiflist=","elong=","biaslist=","elongdata="])
	except getopt.GetoptError, error:
		sys.stderr.write(str(error)+"\n")
		usage()
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit()
		elif opt =="--testprefix":
			testprefix = arg
		elif opt == "--trials" :
			trials = int(arg)
		elif opt == "--maxStrands" :
			max_strand_nr = int(arg)
		elif opt == "--maxStrandLength" :
			maxStrandLength = int(arg)
		elif opt == '--numCells' :
			numCells = int(arg)
		elif opt == '--numRounds' :
			numRounds = int(arg)
		elif opt == '--motiflist' :
			motiflist = []
			tail = arg
			for comma in range(arg.count(',')+1):
				head,sep,tail = tail.partition(',')
				motiflist.append(head)
		elif opt == '--elong' :
			elong = float(arg)
		elif opt == '--biaslist' :
			biaslist = []
			tail = arg
			for comma in range(arg.count(',')+1):
				head,sep,tail = tail.partition(',')
				biaslist.append(head)
			biaslist = [float(bias) for bias in biaslist]
		elif opt == '--elongdata' :
			elongdata = arg
		else:
			sys.stderr.write("Unknown option %s\n" %opt)
			usage()
			sys.exit(2)

	if len(biaslist) != len(motiflist):
		sys.stderr.write("motiflist and biaslist must be of the same length")
		usage()
		sys.exit(3)

	masterprefix = 'MotifCompeteSimulation_'

	parameterlist = [trials, max_strand_nr, maxStrandLength, numCells, numRounds, motiflist, elong, biaslist]

	pop_tracker, nr_strands_per_time, elongation_tracker = motifcompetesim_motifoutput(parameterlist,masterprefix,testprefix,trials,max_strand_nr,maxStrandLength,numCells,numRounds,motiflist,elong,biaslist)

	motifcompetesim_fulltrialoutput(parameterlist,masterprefix,testprefix,pop_tracker[0],elongation_tracker[0],trials,max_strand_nr,maxStrandLength,numCells,numRounds,motiflist,elong,biaslist)

	strand_number_dict = motifcompetesim_allstrandoutput(parameterlist,masterprefix,testprefix,pop_tracker,nr_strands_per_time,trials,max_strand_nr,maxStrandLength,numCells,numRounds,motiflist,elong,biaslist)

	try:
		elongdata
	except:
		elongdata =  'False'

	if elongdata == 'True':
		motifcompetesim_elongdataoutput(parameterlist,masterprefix,testprefix,pop_tracker,nr_strands_per_time,elongation_tracker,strand_number_dict,trials,max_strand_nr,maxStrandLength,numCells,numRounds,motiflist,elong,biaslist)



if __name__ == "__main__":
	main(sys.argv[1:])







