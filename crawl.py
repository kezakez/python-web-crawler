import sys
import httplib
import re

url = "http://www.hackernews.net"
depth = 2
search = "python"

# get the parameters or use defaults
if (len(sys.argv) > 1):
	url = sys.argv[1]	

if (len(sys.argv) > 2):
	depth = int(sys.argv[2])

if (len(sys.argv) > 3):
	search = sys.argv[3]

processed = []

def searchURL(url, depth, search):
	# only do http links
	if (url.startswith("http://") and (not url in processed)):
		processed.append(url)
		url = url.replace("http://", "", 1)
		
		# split out the url into host and doc
		host = url
		path = "/"

		urlparts = url.split("/")
		if (len(urlparts) > 1):
			host = urlparts[0]
			path = url.replace(host, "", 1)

		# make the first request
		print "crawling host: " + host + " path: " + path
		conn = httplib.HTTPConnection(host)
		req = conn.request("GET", path)
		res = conn.getresponse()

		# find the links
		contents = res.read()
		m = re.findall('href="(.*?)"', contents)
		
		if (search in contents):
			print "Found " + search + " at " + url

		print str(depth) + ": processing " + str(len(m)) + " links"
		for href in m:
			# do relative urls
			if (href.startswith("/")):
				href = "http://" + host + href

			# follow the links
			if (depth > 0):
				searchURL(href, depth-1, search)
	else:
		print "skipping "	+ url
		
searchURL(url, depth, search)
