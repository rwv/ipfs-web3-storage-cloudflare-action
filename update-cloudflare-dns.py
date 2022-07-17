import urllib.request
import json
import os

DOMAIN = os.environ['DOMAIN']
ZONE_ID = os.environ['ZONE_ID']
CLOUDFLARE_API_TOKEN = os.environ['CLOUDFLARE_API_TOKEN']
CID = os.environ['CID']

url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records?type=TXT&name=_dnslink.{DOMAIN}"

req = urllib.request.Request(url=url, headers={
    "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
    "Content-Type": "application/json",
}, method='GET')
res = urllib.request.urlopen(req)
res_body = res.read()

# https://docs.python.org/3/library/json.html
data = json.loads(res_body.decode("utf-8"))

if not data["success"]:
    raise Exception("Failed to fetch DNS records", data)

cloudflare_record_id = data["result"][0]["id"]

url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/{cloudflare_record_id}"

put_data = {
    "type": "TXT",
    "name": f"_dnslink.{DOMAIN}",
    "content": f"dnslink=/ipfs/{CID}",
    "ttl": 60,
    "proxied": False
}

req = urllib.request.Request(url=url, headers={
    "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
    "Content-Type": "application/json",
}, method='PUT', data=json.dumps(put_data).encode("utf-8"))

res = urllib.request.urlopen(req)
res_body = res.read()

data = json.loads(res_body.decode("utf-8"))

print(data)
