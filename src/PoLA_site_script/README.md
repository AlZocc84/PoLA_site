### Prerequisites
predict_adsorption.py requires a series of python packages to work. These can be obtained through  via
```
git clone https://github.com/AlexMoreo/porous-materials.git
cd porous-materials
python3 -m venv .venv
source .venv/bin/activate
pip install numpy pandas scikit-learn matplotlib joblib
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```
or with conda:
```
conda create -n porous python=3.12  
conda activate porous  
pip install numpy pandas scikit-learn matplotlib joblib  
pip install torch torchvision --index-url [https://download.pytorch.org/whl/cpu](https://download.pytorch.org/whl/cpu)
```
We suggest to add the src directory included to your path, or to define an alias for src/predict_adsorption.py .
### Instructions
The script can be executed via the command
```
predict_adsorption.py -isotherm 
<isotherm_file> --output <output_prefix> 
--format <format> --method <method>
```
where:
- ```isotherm_file``` is the location of the file containing the $N_2$ excess adsorption isotherm to use as input.
- ```output_prefix``` is the prefix to be added to the output files. The file is expected to contain two columns of numbers. The first is the loading pressure, the second the corresponding excess adsorption (see the  ```--format``` keyword). 
- ```format``` describes the units in which the adsorption is measured. Available options are $mol/g$ (option  ```mol```) and  $CC(STP)/g$  (option```cc```). The default option is ```mol```.
- ```method``` describes the neural regressor model employed. It should not be useful to most users. Available options are 
	- ```regular```
	- ```with_exp```
	- ```cut```  
	- ```partial```
### Results
The script produces .dat files and .png for 
- the VminD porous volume characterization, 
- cumulative VminD
- simplified VminD histograms
- predicted $H_2$ adsorption at 77K.
