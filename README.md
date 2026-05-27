# PoLA_site
Repository for the files needed by the PoLA website

All the python code is present in the [src](src) folder.

The python packages required can be installed with 

```git clone https://github.com/AlexMoreo/porous-materials.git
cd porous-materials
python3 -m venv .venv
source .venv/bin/activate
pip install numpy pandas scikit-learn matplotlib joblib
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

or, if you prefer Conda, with:

```
conda create -n porous python=3.12
conda activate porous
pip install numpy pandas scikit-learn matplotlib joblib
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

The manual can be found [here](/src/PoLA_site_script/README.md)
