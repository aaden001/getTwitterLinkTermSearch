# collect-links-cursor.py
# MCW - 2/11/2021
import sys
import tweepy
import requests # for  requesting the url
from urllib.parse import urlparse # for requesting parse

def resovle_url(base_url,count):
    #print("\nProcess:    " +base_url +"\n")
    try:
        request = requests.head(base_url,allow_redirects=True,timeout=2.5)     
        if (request.status_code == 200):
            domain = urlparse(request.url).netloc
            if domain.find("twitter.com") ==-1:
                print("{} {}    :      {}".format( count,base_url,request.url))
                print("\n")
            else:
                count = count -1      
        else:
            count = count -1
        request.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        pass
        #print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        count = count -1
        #print(f'Other error occurred: {err}')    
    return  count

# use coronavirus as default search term unless one provided
search_term = "coronavirus"
if len(sys.argv) > 1:
     search_term = str(sys.argv[1])

# number of links to collect
MAX_COUNT = 100
count = 1

# OAuth2 procedure
consumer_key = "pnUItdX31QmYpHBFlVcYbocKQ"      # INSERT YOUR KEY HERE
consumer_secret = "gFNX2iztwhfL1tROFCX3UomwRbU8GjUJhHzLQat8DGxvBcyVmw"   # INSERT YOUR KEY HERE
auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)

try:
  for page in tweepy.Cursor(api.search, q=search_term, tweet_mode='extended', lang='en').pages():
    for tweet in page:
         for link in tweet.entities["urls"]:
             count = resovle_url(link['expanded_url'],count)
             count = count + 1
    if count > MAX_COUNT or count == 100:
         break
except tweepy.TweepError as e:
  print ("Tweepy Error: %s" % str(e))
