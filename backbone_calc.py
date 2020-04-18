from Bio.PDB import *
from math import sqrt
import numpy as np
from sys import argv
import os
import multiprocessing as mp
import statistics
import argparse

AAs = ['ALA','CYS','ASP','GLU','PHE','GLY','HIS','ILE','LYS','LEU','MET','ASN','PRO','GLN','ARG','SER','THR','VAL','TRP','TYR']

parser = argparse.ArgumentParser(description='Calculate the Ca-C bond lengths of protein structures')
parms = parser.add_argument_group('Required parameters')
parms.add_argument("-d","--directory",action='store', type=str, help="The directory of the PDB files in .pdb or .cif format.",dest='directory',default='')
parms.add_argument("-n","--name",action='store', type=str, help="The name to give the summary file.",dest='name',default='')
parms.add_argument("-t", "--threads",action='store', type=int, help="Number of threads to run in parallel. Default is 1.",dest='threads',default=1)
parms.add_argument("-i", "--individual",action='store_true', help="Save a list of Ca-C distances for each structure.",dest='indiv',default=False)
args = parser.parse_args()

name = args.name
directory = args.directory
threads = args.threads
indiv = args.indiv

def distance(position):
	try:
		pos_a = position['CA'].get_coord()
		pos_b = position['C'].get_coord()
	except:
		return np.nan
	else:
		return sqrt(sum([(pos_a[x]-pos_b[x])**2 for x in range(0,3,1)]))

def calc(name):
	if name.split('.')[-1] == 'pdb':
		p = PDBParser()
		structure = p.get_structure(name.split('/')[-1].split('.')[0], name)
		method = structure.header['structure_method']
		date = structure.header['deposition_date']
		resolution = structure.header['resolution']
	else:
		p = MMCIFParser()
		structure = p.get_structure(name.split('/')[-1].split('.')[0], name)
		header = MMCIF2Dict.MMCIF2Dict(name)
		method = header['_exptl.method'][0]
		date = header['_pdbx_database_status.recvd_initial_deposition_date'][0]
		resolution = None #mmcif resolution annotation is unclear between xray and em
	dist_1 = [distance(residue) for structs in structure for chain in structs for residue in chain if residue.get_resname() in AAs]
	mean = statistics.mean(dist_1)
	median = statistics.median(dist_1)
	if indiv:
		return {'name':'.'.join(name.split('/')[-1].split('.')[:-1]),'mean':mean,'method':method,'date':date,'resolution':resolution,'median':median,'list':dist_1}
	else:
		return {'name':'.'.join(name.split('/')[-1].split('.')[:-1]),'mean':mean,'method':method,'date':date,'resolution':resolution,'median':median}

def runner(model):
	#return calc(model)
	try:
		result = calc(model)
	except:
		return None
	else:
		return result

models = [directory+file for file in os.listdir(directory) if file.split('.')[-1] in ['pdb','cif']]
pool = mp.Pool(threads)
distances = pool.map(runner,models)
pool.close()
pool.join()
#distances = map(runner,models)
distances= list(distances)

with open(name+'_Ca-C_distances.tsv','w') as f:
	f.write('model\tdeposition_date\tmethod\tresolution\tdistance_mean\tdistance_median\n')
	for distance in distances:
		if not(distance == None):
			f.write(distance['name']+'\t'+str(distance['date'])+'\t'+str(distance['method'])+'\t'+str(distance['resolution'])+'\t'+str(distance['mean'])+'\t'+str(distance['median'])+'\n')

if indiv:
	for distance in distances:
		with open(distance['name']+'_Ca-C_distances.txt','w') as f:
			f.write('\n'.join([str(x) for x in distance['list']]))