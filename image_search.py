import re
from collections import Counter
from mrcc import CCJob
import threading
import argparse

threadLimit = threading.Semaphore(30)

class myThread (threading.Thread):
    def __init__(self, threadID, url):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.url = url
    def run(self):
        try:
           print "Starting thread" + str(self.threadID)
           fetch_image(self.url)
        finally:
           print "Exiting thread" + str(self.threadID)
           threadLimit.release()

def fetch_image(url):
    import socket
    socket.setdefaulttimeout(10)
    import urllib 
    try:
       urllib.urlretrieve(url, filename='/data/output/'+url.split('/')[-1])
       print ('download complete') 
    except:
       print ("URL not found or the image is no longer available")
    return
 		
# Optimization: compile the regular expression once so it's not done each time
# The regular expression looks for (1) a tag name using letters (assumes lowercased input) and numbers
# and (2) allows an optional for a space and then extra parameters, eventually ended by a closing >
HTML_TAG_PATTERN = re.compile('<([a-z0-9]+)[^>]*>')
URL_TAG = re.compile('GET(.*?)HTTP')
HOST_TAG = re.compile('Host(.*)')
# Regex to read image source and alt text
IMAGE_TAG = re.compile('<img.*?src="([^"]*)".*?alt="([^"]*)".*?>')

def get_images(data):
  ctr = IMAGE_TAG.findall(data)
  return ctr
	
	

class TagCounter(CCJob):
  def process_record(self, record, tags):
    # WARC records have three different types:
    #  ["application/warc-fields", "application/http; msgtype=request", "application/http; msgtype=response"]
    # We're only interested in the HTTP responses
    if record['Content-Type'] == 'application/http; msgtype=response':
       url = record.url
       payload = record.payload.read()
       header, body = payload.split('\r\n\r\n', 1)
       ext = tags.split(',')
       if any(x.strip() in url for x in ext) and 'Content-Type: text/html' in header:
       # We avoid creating a new Counter for each page as that's actually quite slow
         urls = get_images(body)
         if len(urls) > 0:           
	    for i, a in enumerate(urls): 
                if a[0].startswith('http') and any(x.strip() in a[1] for x in ext):
                    thread = myThread(i, a[0])
                    threadLimit.acquire()
 		    thread.start() 
         yield 'test',len(urls)    
         self.increment_counter('commoncrawl', 'processed_pages', 1)

if __name__ == '__main__':
    TagCounter.run()
