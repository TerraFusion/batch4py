#!/bin/bash

export PYTHONUSERBASE="${HOME}"
sudo python setup.py install

echo "testing batch4py importability..."
python -c "import batch4py"
echo "done"

