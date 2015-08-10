import time
import praw
import re
import os
from redditbot_info import *


r = praw.Reddit('Wikipedia Mobile to Desktop Link Converter v0.1 (by /u/GoCubs10)')

client_id, client_secret, redirect_uri = redditbotdata()
r.set_oauth_app_info(client_id, client_secret, redirect_uri) 
authenticated_user, access_token = get_token()

scopes = ['identity', 'edit', 'submit', 'read', 'save']
r.set_access_credentials(set(scopes), access_token, refresh_token=None, update_user=True)
print authenticated_user.name, authenticated_user.link_karma



fname = 'replied_comments.txt'

content = []
if os.path.exists(fname):
    with open(fname) as f:
        for line in f:
            content.append(line.replace('\n', ''))

print content

replied = open(fname, 'a+')

time1 = time.time()

while True:
    commented = 0
    
    time2 = time.time()
    #print time2 - time1
    if time2 - time1 > 2700:
        authenticated_user, access_token = get_token()
        r.set_access_credentials(set(scopes), access_token, refresh_token=None, update_user=True)
        time1 = time.time()
    
    subreddit = r.get_subreddit('funny+todayilearned+aww+gaming+videos+gifs+showerthoughts+news+worldnews+politics+'
                                +'mildlyinteresting+movies+food+jokes+oldschoolcool+earthporn+explainlikeimfive')
    comments = subreddit.get_comments(limit=5000)
   # comments = r.get_comments('all')

    for comment in comments:
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', comment.body)
        for link in urls:
            if 'en.m.wikipedia.org' in link:
                lshort =  link.replace('en.m.wiki', 'en.wiki')
                if lshort[-1] == ':':
                    lshort = lshort[:-1]
                if lshort[-1] == '.':
                    lshort = lshort[:-1]
                if lshort[-1] == ',':
                    lshort = lshort[:-1]  
                if (lshort[-1] == ')') and (lshort.count(')') > lshort.count('(')):
                    lshort = lshort[:-1]
                #print comment.id
                if comment.id in content:
                    pass
                else:
                    lshort = lshort.replace(')', '\)')
                    replied.write(comment.id +'\n')
                    content.append(comment.id)
                    #print content
                    #print lshort
                    #print comment
                    #print ('It looks like you included a link to mobile Wikipedia. [Here]('+lshort +') is the desktop site!')
                    comment.reply('It looks like you included a link to mobile Wikipedia. [Here]('+lshort +') is the desktop site!')
                    commented = 1

        if commented == 1:
            print 'Posted to ' +comment.id
            print 'sleeping for two minutes...'
            time.sleep(120)
            break

    