#!/bin/bash

export PYTHONUSERBASE="${HOME}"
sudo python setup.py install

echo "testing batch4py importability..."
python -c "import batch4py"
echo "done"

echo "Performing batch4py test suite..."
python tests/import.py
echo "Done"

