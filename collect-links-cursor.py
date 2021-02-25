# collect-links-cursor.py
# MCW - 2/11/2021
import sys
import tweepy
import requests # for  requesting the url
from urllib.parse import urlparse # for requesting parse


def resovle_url(base_url,count):
    #print("\nProcess:    " +base_url +"\n")
    value =0
    url=""
    try:
        request = requests.head(base_url,allow_redirects=True,timeout=2.5)     
        if (request.status_code == 200):
            domain = urlparse(request.url).netloc
            if domain.find("twitter.com") ==-1:
                url  = request.url
                value =1
                """
                print("{} {}    :      {}".format( count,base_url,request.url))
                print("\n")
                if(blank_dict.get(request.url) != None):
                    pass
                else:
                    #store link
                    blank_dict[request.url] = count
                """
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
    return  count,value, url

# use coronavirus as default search term unless one provided
search_term = "coronavirus"
if len(sys.argv) > 1:
     search_term = str(sys.argv[1])

# number of links to collect
MAX_COUNT = 1000
count = 1
url =""
value =0

blank_dict ={}

# OAuth2 procedure
consumer_key = "pnUItdX31QmYpHBFlVcYbocKQ"      # INSERT YOUR KEY HERE
consumer_secret = "gFNX2iztwhfL1tROFCX3UomwRbU8GjUJhHzLQat8DGxvBcyVmw"   # INSERT YOUR KEY HERE
auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)

try:
  for page in tweepy.Cursor(api.search, q=search_term, tweet_mode='extended', lang='en').pages():
    for tweet in page:
         for link in tweet.entities["urls"]:
             count,value, url = resovle_url(link['expanded_url'],count)
             #print(count)
             
             if value != 0 :
                 if(blank_dict.get(url) != None):
                    count = count - 1
                 else:
                    #store link
                    print(count)
                    print(url)
                    blank_dict[url] = count
             count = count + 1       
    if count > MAX_COUNT:
        print("\n\n")
        print(len(blank_dict))
        for x in range(0,len(blank_dict)-MAX_COUNT):
            blank_dict.popitem()
        print(len(blank_dict))
        # swap
        blank_dict = {value:key for key, value in blank_dict.items()}
        myfile = "dict.txt"
        with open(myfile, 'w') as f: 
            for key, value in blank_dict.items(): 
                f.write('%s' % (value)) 
        break
except tweepy.TweepError as e:
  print ("Tweepy Error: %s" % str(e))
