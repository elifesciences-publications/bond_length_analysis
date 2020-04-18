
from Bio.PDB import *
from math import sqrt
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
import numpy as np
from sys import argv
import os
import gzip
import multiprocessing as mp
from tqdm import tqdm
import statistics

AAs = ['ALA','CYS','ASP','GLU','PHE','GLY','HIS','ILE','LYS','LEU','MET','ASN','PRO','GLN','ARG','SER','THR','VAL','TRP','TYR']

atom1 = 'CA'
atom2 = 'C'
name = argv[1]
directory = argv[2]
threads = int(argv[3])

def distance(position):
	try:
		pos_a = position[atom1].get_coord()
		pos_b = position[atom2].get_coord()
	except:
		return np.nan
	else:
		return sqrt(sum([(pos_a[x]-pos_b[x])**2 for x in range(0,3,1)]))

def calc(name):
	p = PDBParser()
	structure = p.get_structure(name.split('/')[-1].split('.')[0], name)

	dist_1 = [distance(residue) for structs in structure for chain in structs for residue in chain if residue.get_resname() in AAs]
	mean = statistics.mean(dist_1)
	median = statistics.median(dist_1)
	return {'name':'.'.join(name.split('/')[-1].split('.')[:-1]),'mean':sum(dist_1)/len(dist_1),'method':structure.header['structure_method'],'date':structure.header['deposition_date'],'resolution':structure.header['resolution'],'median':median}

def runner(model):
	try:
		result = calc(model)
	except:
		return None
	else:
		return result

models = [directory+file for file in os.listdir(directory) if file.split('.')[-1] == 'pdb']
pool = mp.Pool(threads)
distances = pool.map(runner,models)
pool.close()
pool.join()
#distances = map(runner,tqdm(models,unit='models'))
distances= list(distances)

with open(name+'_Ca-C_distances.tsv','w') as f:
	f.write('model\tdate\tmethod\tresolution\tdistance_mean\tdistance_median\n')
	for distance in distances:
		if not(distance == None):
			f.write(distance['name']+'\t'+str(distance['date'])+'\t'+str(distance['method'])+'\t'+str(distance['resolution'])+'\t'+str(distance['mean'])+'\t'+str(distance['median'])+'\n')
