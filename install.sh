#!/bin/bash

export PYTHONUSERBASE="${HOME}"
sudo python setup.py install
python -c "import batch4py"


