PYTHON="./.venv/bin/python3"

rm -rf dist/
$PYTHON -m build

if [ "$1" == "--upload" ]
then
    $PYTHON -m twine upload --repository pypi dist/*
fi