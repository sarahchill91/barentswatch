# barentswatch readme

Baseline code here was developed based on a set of python files that demonstrate the use of Barentswatch API, so some files (e.g., authentication.py will be very similar): https://github.com/barentswatch/barentswatch-api-examples
The official API documentation is here: https://wiki.barentswatch.net/display/BO/Application+registration+and+authentication

Python3 is required and the package requests needs to be installed:
``` bash
> pip3 install requests pydantic
```


Get Usage``` bash
> python3 authentication.py --id your_id --secret your_secret
```
E.g., python3 authentication.py --id sahill@rvc.ac.uk:SarahHill --secret putpasswordhere