# smsbrute.py

A simple tool to demonstrate brute-forcing weak to no security APIs that use x-digit passcodes e.g for password recovery. This tool is for educational purposes only, don't be that snowflake who hacks others. Even with mediocre scripts, comes great responsibility and doing something unlawful is on your liability! A test API for this script can be found from [HERE](https://github.com/miikkaak/)

## Usage
Change the URL and modify the custom parameters that are sent within the POST request
```
url         =   "http://localhost:8081/"  #API url. MODIFY THIS!
```
AND
```
params = {"id" : 1, "name" : "test", "smscode" : "%s" % param} #POST request paramters. MODIFY THIS!
```
From terminal:
```
Usage: python3 ./smsbrute [-max number of passcodes]
```