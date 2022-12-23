rm dist/*
python -m build
if [ "$1" == "--upload" ]
then
    python3 -m twine upload --repository pypi dist/*
fi