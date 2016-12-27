import praw
import json

# What position on r/all would you like to post the comment on?
notificationThreshold = 100

# What subreddit?
subreddit = 'pcmasterrace'

# The message you want to send.  Use Reddit formatting here.
allMessage = """Hey, this is on r/all.
[Read the rules you numpties.](/r/pcmasterrace/about/rules)"""

# http://praw.readthedocs.io/en/v4.0.0/getting_started/authentication.html?highlight=oauth
# You will definitely have to change this.  See the above link for instructions

auth = {}
auth['client_id'] = ''
auth['client_secret'] = ''
auth['user_agent'] = 'r/all watcher example by Eegras'
auth['username'] = ''
auth['password'] = ''

reddit = praw.Reddit(client_id=auth['client_id'],
                     client_secret=auth['client_secret'],
                     password=auth['password'],
                     user_agent=auth['user_agent'],
                     username=auth['username'])

fn = './seenFrontPagePosts.txt'

try:
    f = open(fn, 'r+')
except IOError:
    f = open(fn, 'w+')

try:
    frontOld = json.loads(f.readline())
except:
    frontOld = []

# Get the top N posts from Reddit.  N is notificationThreshold
redditFrontPage = reddit.front \
                        .hot(limit=notificationThreshold)

# Loop through each post
for post in redditFrontPage:
    # See if the subreddit that the post is in is the subreddit
    # we care about.
    if str(post.subreddit) == subreddit:
        print "We have a post on r/all! '{}'".format(post.title)
        if str(post.id) not in frontOld:
            print "We haven't seen it before!"
            message = post.reply(allMessage)
            message.distinguish(sticky=True)

            frontOld.append(str(post.id))
        else:
            print "We have seen it before."
    f.seek(0)
    f.truncate()
    f.seek(0)
    f.write(json.dumps(frontOld))
    f.close()
