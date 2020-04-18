#/usr/bin/bash

mkdir pdb/
cd pdb/
sed -e 's/^/https:\/\/files.rcsb.org\/download\//; s/$/.pdb/' ../test.tsv > ../test2.tsv
wget -i ../test2.tsv
#sed -e 's/^/https:\/\/files.rcsb.org\/download\//; s/$/.pdb/' ../PDBj_cryoem.tsv > ../PDBj_cryoem_mod.tsv
#wget -i ../PDBj_cryoem_mod.tsv
#sed -e 's/^/https:\/\/files.rcsb.org\/download\//; s/$/.pdb/' ../PDBj_xray.tsv > ../PDBj_xray_mod.tsv
#wget -i ../PDBj_xray_mod.tsv
cd ..

python3 backbone_calc_ideal.py ./pdb/ 4