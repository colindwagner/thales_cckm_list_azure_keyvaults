
import requests
import json
import sys
requests.urllib3.disable_warnings()
session = requests.Session()
session.verify = False

#URL HERE
domain_name = "cckm.acme.net
cckm_url = "https://" + domain_name + ":8443/kmaas/"
resp = session.get(cckm_url)

# For Azure service principal login
# Replace your tenant name and tenant password
tenant = sys.argv[1]
password = sys.argv[2]
session.headers = {'X-XSRF-TOKEN': resp.headers['X-XSRF-TOKEN']}
data = {'tenant': tenant, 'password': password}
resp = session.post(cckm_url + "auth2/azure", data=data)

if resp.status_code != 200:
    print(resp.content)
    sys.exit()

session.headers['Content-Type'] = 'application/json'

def call_api(method, api, data=data):
    print("Accessing...." + cckm_url + api)
    if method == 'post':
      resp = session.post(cckm_url + api, data=json.dumps(data))
    elif method == 'put':
      resp = session.put(cckm_url + api, data=data)
    else:
      resp = session.get(cckm_url + api)
      print("%s %s" % (method, api))
    if data:
      print(data)
      print(json.dumps(resp.json(), indent=4))
    return resp.json()


source_key = call_api("get", "rest/azureKeyVaults")

resp = session.post(cckm_url + "logout")
