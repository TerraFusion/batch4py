#!/bin/bash

export PYTHONUSERBASE="${HOME}"
sudo python setup.py install

echo "testing batch4py importability..."
python -c "import batch4py"
retval=$?
echo "done"
if [ $retval -ne 0 ]; then
    exit $retval
fi

echo "Performing batch4py test suite..."
sudo python tests/simple.py
retval=$?
echo "Done"

if [ $retval -ne 0 ]; then
    exit $retval
fi
