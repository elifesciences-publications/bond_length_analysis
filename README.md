This code is associated with the paper from  Sauer et al., "Structural basis for the reaction cycle of
DASS dicarboxylate transporters". eLife, 2020. http://doi.org/10.7554/eLife.61350

# bond_length_analysis
Calculate the average backbone Ca-C distances for PDB files. 

Results included for the Top500 and Top8000 datasets of high resolution structures, and recent X-ray and CryoEM structures.

Run script with the following command:
```
python3 backbone_calc.py -n name_of_output_file -d directory_of_PDB_files -t threads
```
note: Include -i if you want to save all the Ca-C distances for a each PDB file. 
