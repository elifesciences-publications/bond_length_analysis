#/usr/bin/bash

wget http://kinemage.biochem.duke.edu/php/downlode.php?filename=/downloads/datasets/top500H.tgz -O top500H.tgz
tar -zxvf top500H.tgz
for f in ./top500H/*
do 
	mv $f $f.pdb
done
python3 backbone_calc.py Top500 ./top500H/ $1

wget http://kinemage.biochem.duke.edu/php/downlodekins.php?filename=/downloads/datasets/top8000_chains_70.tgz -O top8000_chains_70.tgz
tar -zxvf top8000_chains_70.tgz
python3 backbone_calc.py Top8000 ./top8000_chains_70/ $1
