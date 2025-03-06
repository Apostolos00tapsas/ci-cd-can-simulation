# ci-cd-can-simulation
# CAN Bus Simulation
For  CAN Bus Simulation install python can library as:
```
pip install python-can can-isotp pytest allure-pytest
pip install cantools
```


# Run Testcanfile 
Test can file contains the testcases and can be executed as:
```
pytest test_can.py -s
```

# Possible problems
In case that pytest test_can.py -s rerutns:
```
DeprecationWarning: the imp module is deprecated in favour of importlib and slated for removal in Python 3.12; see the module's documentation for alternative uses
    from imp import reload
-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
```
try: 
```
pip install --upgrade future
```

# Reinstall python-can and clean cache 
In case python-can saves any unnecesery file try:
```
pip uninstall python-can
pip install python-can --no-cache-dir
```

