# WayBacker

A simple python script for subdomain and parameter discovery using the wayback machine!

### usage 

```
usage: python3 waybacker.py [-h] -d DOMAIN --mode MODE [-mime MIME] [--silent]

OPTIONS:
  -h, --help            show this help message and exit
  -d DOMAIN, --domain DOMAIN
                        Domain name to enumerate
  --mode MODE           Value can be subs/params/all to grab subdomains/parameters/both
  --mime MIME            Return files with specific mimetype. e.g - application/json,text/html etc
  --silent              Print only the output

Example: python waybacker.py -d google.com
```