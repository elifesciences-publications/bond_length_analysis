#/usr/bin/bash

mkdir cryoem/
cd cryoem/
sed -e 's/^/https:\/\/files.rcsb.org\/download\//; s/$/.pdb/' ../PDB_cryoem.tsv > ../PDB_cryoem_mod.tsv
wget -i ../PDB_cryoem_mod.tsv
cd ..
python3 backbone_calc.py cryoem ./cryoem/ $1

mkdir xray/
cd xray/
sed -e 's/^/https:\/\/files.rcsb.org\/download\//; s/$/.pdb/' ../PDB_cryoem.tsv > ../PDB_cryoem_mod.tsv
wget -i ../PDB_cryoem_mod.tsv
cd ..
python3 backbone_calc.py xray ./xray/ $1
