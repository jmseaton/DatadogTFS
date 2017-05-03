#!/usr/bin/python
import requests, json, csv, ConfigParser

# config file named datadog-config 
# this should contain two vars: api_key, app_key
#with open("datadog_config.py", 'w') as datadog_config:

ddcfg = ConfigParser.RawConfigParser()
ddcfg.read('datadog.cfg')

par=dict(ddcfg.items("Settings"))
for p in par:
	par[p]=[p].split("#",1)[0].strip() # remove inline comment

globals().update(par)

url = "https://app.datadoghq.com/reports/v2/overview?api_key="+api_key+"&application_key="+app_key+"&window=3h&metrics=avg%3Asystem.cpu.idle%2Cavg%3Aaws.ec2.cpuutilization%2Cavg%3Avsphere.cpu.usage%2Cavg%3Aazure.vm.processor_total_pct_user_time%2Cavg%3Asystem.cpu.iowait%2Cavg%3Asystem.load.norm.15&with_apps=true&with_sources=true&with_aliases=true&with_meta=true&with_mute_status=true&with_tags=true"
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
r = requests.get(url,headers=headers)

def get_datadog_hosts(data):
	host_agent = agent_version(data)
	keys = host_agent[0].keys()
	with open ("datadog-hosts.out",'w') as outfile:
		csv_file = csv.writer(outfile)
		for rows in host_agent:
			ele = []
			for key in keys:
	 			ele.append(rows[key])
			csv_file.writerow(ele)

def agent_version(data):
	host_agent = []
	for hosts in data["rows"]:
		if "agent_version" in hosts["meta"]:
#			print hosts["host_name"]
			host_agent.append({"host_name": hosts["host_name"]})
	return host_agent

if r.status_code == 200:
	data = r.json()
	get_datadog_hosts(data)
