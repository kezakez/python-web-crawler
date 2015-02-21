import httplib
import re
import argparse


def searchURL(url="http://www.hackernews.net", depth=2, search="python"):
        processed = []
	# only do http links
	if url.startswith("http://") and (not url in processed):
		processed.append(url)
		url = url.replace("http://", "", 1)
		
		# split out the url into host and doc
		host, path = url, "/"

		urlparts = url.split("/")
		if len(urlparts) > 1:
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
		
		if search in contents:
			print "Found " + search + " at " + url

		print str(depth) + ": processing " + str(len(m)) + " links"
		for href in m:
			# do relative urls
			if href.startswith("/"):
				href = "http://" + host + href

			# follow the links
			if depth:
				searchURL(href, depth-1, search)
	else:
		print "skipping " + url

def main():
    parser = argparse.ArgumentParser(description="python web crawler")
    parser.add_argument('url',help='url to be crawled')
    parser.add_argument('depth',type=int,help='depth levels which means go into links on a page till depth level')
    parser.add_argument('search',help='search text')
    args = parser.parse_args()
    
    searchURL(args.url, args.depth, args.search)
    		
if __name__== '__main__':
    main()    
