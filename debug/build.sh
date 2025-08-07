PYTHON="/home/jbarnart/.pyenv/shims/python"

rm -rf dist/
$PYTHON -m build

if [ "$1" == "--upload" ]
then
    $PYTHON -m twine upload --repository pypi dist/*
fi