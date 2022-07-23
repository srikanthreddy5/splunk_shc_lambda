# splunk_shc_lambda

## Create a  python layer
```

mkdir  python ; cd python 
pyenv local 3.8.10
mkdir myPythonLayer/python
pip  install requests -t .
pip install boto3 -t .
cd  ..
zip -r python.zip python

```
