import requests
import os
import json
import sys
import logging
import csv
import time

devices = []
sources = []
my_sources = {}
rows = {}
DAYS_BACK = 7
start = time.time() - (86400*DAYS_BACK)
page = 1
per_page = 100
header = ["Sevco ID","Timestamp","Names","FQDN","IP","MAC","Manufacturer","OS","OS Category","Recent Users","Groups","Distinguished Name"]

if not os.environ.get("JWT"):
    raise Exception("Need API key in JWT environment variable.")
if not os.environ.get("ORG"):
    raise Exception("Need target org id in ORG environment variable.")

org = os.environ['ORG']
token = os.environ['JWT']

# Grab a list of sources to build header
r = requests.get("https://dev.api.sevcolabs.com/v1/integration/source",
                 headers={ 'Authorization': token, 'X-Sevco-Target-Org': org})
r.raise_for_status()
sources = r.json()

# Grab a list of integrations configured for the org
r = requests.get("https://dev.api.sevcolabs.com/v1/integration/source/config",
                 headers={ 'Authorization': token, 'X-Sevco-Target-Org': org})
r.raise_for_status()
integrations = r.json()

# Make a Dictionary of display names and source_types to allow dynamic generation of the header and pulling of source unique identifiers
for integration in integrations:
    for source in sources:
        if source["id"] == integration["source_id"]:
            my_sources[source["display_name"]] = source["source_type"]

# Build the Devices JSON structure
while True:
    r = requests.get("https://dev.api.sevcolabs.com/v1/asset/device",
                     headers={'Authorization': token, 'X-Sevco-Target-Org': org},
                     params={'start': start, 'per_page': per_page, 'page': page})

    r.raise_for_status()
    data = r.json()
    if len(data['items']) == 0: break

    devices.extend(data['items'])
    page += 1

# Add the sources to the header
header = header + list(my_sources.keys())

# Parse the JSON structure and write the csv file
with open ('devices.csv', 'w', newline='') as csvfile:
    fieldnames = header
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for device in devices:
        row = []
        row.append(device['id'])
        row.append(device['timestamp'])

        if 'hostname' in device['attributes'].keys():
          row.append(device['attributes']['hostname']['value'])
        else:
            row.append("")

        if 'fqdn' in device['attributes'].keys():
            row.append(device['attributes']['fqdn']['value'])
        else:
            row.append("")

        if 'ips' in device['attributes'].keys():
            row.append(device['attributes']['ips']['value'])
        else:
            row.append("")
    
        if 'mac_addresses' in device['attributes'].keys():
            row.append(device['attributes']['mac_addresses']['value'])
        else:
            row.append("")

        if 'mac_manufacturers' in device['attributes'].keys():
            row.append(device['attributes']['mac_manufacturers']['value'])
        else:
            row.append("")

        if 'os' in device['attributes'].keys():
            row.append(device['attributes']['os']['value'])
        else:
            row.append("")

        if 'os_category' in device['attributes'].keys():
            row.append(device['attributes']['os_category']['value'])
        else:
            row.append("")

        if 'recent_users' in device['attributes'].keys():
            row.append(device['attributes']['recent_users']['value'])
        else:
            row.append("")

        if 'groups' in device['attributes'].keys():
            row.append(device['attributes']['groups']['value'])
        else:
            row.append("")
    
        if 'distinguished_name' in device['attributes'].keys():
            row.append(device['attributes']['distinguished_name']['value'])
        else:
            row.append("")

        for src in my_sources.values():
            if src in device['metadata']:
                row.append(list(device['metadata'][src].keys()))
            else:
                row.append("")

        for i, column in enumerate(header):
            rows[column] = str(row[i]).replace(", ","\n").replace("'","").replace("[","").replace("]","")

        writer.writerow(rows)

