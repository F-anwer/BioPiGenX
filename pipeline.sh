chmod +x pipeline.sh

mamba install -c conda-forge py3dmol
mamba install -c conda-forge openmmforcefields
mamba install -c conda-forge cython
mamba install -c conda-forge prody
mamba install -c conda-forge freesasa
pip install lightdock
mamba install -c conda-forge nose
mamba install -c conda-forge pathlib
mamba install -c conda-forge biopandas
conda install bioconda::prokka
pip install pycirclize
pip install tqdm
pip install biotite
