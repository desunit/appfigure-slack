from xml.dom import minidom
from dateutil.parser import parse
import urllib2
import json
import config

def downloadRss(url):
    response = urllib2.urlopen(url)
    return response.read()
    
def getText(nodelist):
    rc = []
    for node in nodelist.childNodes:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)    
    
def starsToColor(title):
    c = title.count(unichr(0x2605))
    if c < 3: 
	return 'danger'
    elif c < 5:
	return 'warning'
    else:
	return 'good'

    
    
def postToSlack(slackUrl, messages):
    post = {
	"username" : "ReviewsBot",
	"text" : "You have " + str(len(messages)) + " new reviews.", 
	"icon_emoji": ":ghost:",
	"attachments" : messages
    }
    data = json.dumps(post)
    req = urllib2.Request(slackUrl, data)
    response = urllib2.urlopen(req).read()
    if response != "ok":
	raise Exception("Invalid response", response)
    
rss = downloadRss(config.appfigure["rssUrl"])    
xmldoc = minidom.parseString(rss)
messages = []

for review in xmldoc.getElementsByTagName('item'):
    title = getText(review.getElementsByTagName('title')[0])
    link = getText(review.getElementsByTagName('link')[0])
    description = getText(review.getElementsByTagName('description')[0])
    date = parse(getText(review.getElementsByTagName('pubDate')[0]))
    messages.append({
	"title" : title,
	"fallback" : title,
	"color" : starsToColor(title),
	"text" : description + " <" + link + "|Details>",
	"unfurl_links" : True,
	"unfurl_media" : True
    })

#print messages
postToSlack(config.slack["webhookUrl"], messages)
