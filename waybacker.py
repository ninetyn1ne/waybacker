import requests
import json
import sys
import argparse
import threading

def parse_args():
    # parse the arguments
    parser = argparse.ArgumentParser(epilog='\tExample: \r\npython ' + sys.argv[0] + " -d google.com")
    parser._optionals.title = "OPTIONS"
    parser.add_argument('-d', '--domain', help="Domain name to enumerate", required=True)
    parser.add_argument('--mode', help='Value can be subs/params/all to grab subdomains/parameters/both', default="",required=True)
    parser.add_argument('--mime', help='Return files with specific mimetype. e.g - application/json,text/html etc')
    parser.add_argument('--silent', help='Print only the output',action='store_true' ,default=False)
    return parser.parse_args()
 
def filtersubs(resjson):
	# Filter subdomains from the JSON response
	#print("[*]Filtering Subdomains.")
	list = []
	for i in range(0,len(resjson)):
		r = resjson[i][0]
		if r != "original":
			r = r.split("/")[2]
			if r not in list:
				list.append(r)
				print(r)
	print("\n")

def getparams(resjson):
	#Get parameters list using wayback machine.
	#print("[*]Grabbing the parameters.")
	params = []
	for i in resjson:
		i = i[0]
		if '?' in i:
			i = i.split('?')[1]
			if '&' in i:
				i = i.split('&')
				for j in i:
					param = j.split('=')[0]
					if param not in params:
						params.append(param)
			else:
				param = i.split('=')[0]
				if param not in params:
					params.append(param)
	for k in params:
		print(k)
	print("\n")

#Parse Response JSON object
def retrievejson(res_json):
	# Print each endpoint from the JSON blob
	for i in range(0,len(res_json)):
		r = res_json[i][0]
		if r != "original":
			print(r)


def wayback(domain,mode):
	# Function to retrieve data from internet archive apis
	#print("[*]Fetching URLs")
	get = requests.get
	if '/' in mode:
		url = "https://web.archive.org/cdx/search?url=%s&matchType=host&collapse=urlkey&fl=original&filter=mimetype:%s&filter=statuscode:200&output=json" % (domain, mode)
	else:
		url = "https://web.archive.org/cdx/search?url=%s&matchType=domain&collapse=urlkey&fl=original&filter=statuscode:200&output=json" % (domain)
	resjson = get(url).json()
	return resjson



def banner():
	print('''

\\   \\  /  \\  /   / /   \\  \\   \\  /   / |   _  \\      /   \\     /      ||  |/  / |   ____||   _  \\     
 \\   \\/    \\/   / /  ^  \\  \\   \\/   /  |  |_)  |    /  ^  \\   |  ,----'|  '  /  |  |__   |  |_)  |    
  \\            / /  /_\\  \\  \\_    _/   |   _  <    /  /_\\  \\  |  |     |    <   |   __|  |      /     
   \\    /\\    / /  _____  \\   |  |     |  |_)  |  /  _____  \\ |  `----.|  .  \\  |  |____ |  |\\  \\----.
    \\__/  \\__/ /__/     \\__\\  |__|     |______/  /__/     \\__\\ \\______||__|\\__\\ |_______|| _| `._____|
===================================================================================================================
																								BY - @ninetyn1ne_
-------------------------------------------------------------------------------------------------------------------
		''')


def main():
	# Main/Driver Function

	#Parse Arguements
	args = parse_args()
	domain = args.domain
	mime = args.mimetype
	mode = args.mode
	silent = args.silent

	#Call function as requested by user.
	if silent==False:
		banner()

	runner = wayback(domain,mime) if mime else wayback(domain,"")
	if mode=="subs":
		filtersubs(runner)
	elif mode == "params":
		getparams(runner)
	elif mode=="all":
		filtersubs(runner)
		getparams(runner)
	else:
		retrievejson(runner)



if __name__=='__main__':
	main()
