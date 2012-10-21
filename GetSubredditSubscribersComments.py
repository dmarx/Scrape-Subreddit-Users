# NOTES
#
#  * Should add associated subreddit to user entry. 
#  * Users should get inserted as they're scraped. Maybe use database
#    to hold users instead of a dict? Or enter users into db as they're
#    entered in the dict

import database as db
#from ScrapeSubUsers import *
from GetSubredditSubscribers import *
import time
import praw

starttime = time.time()

_nposts = 1000


db.init_db()
s = SubredditScraper()

# Approx 2 seconds each post. I.e., each post requires a separate GET request.
# Nice to see that PRAW is regulating GETs. For this step, this interval
# is probably unavoidable.
# 1000 posts ~ 33 minutes
# 994 posts (have we not hit 999 in dc yet?) = 2504 seconds ~ 42 min
# -- 2605 unique users
start = time.time()

# Next line commented out so we can pick up where we left off.
#s.scrapeSubredditUsers(nposts=_nposts)
end = time.time()

print "Time elapsed to scrape %d posts: %d seconds" % (_nposts, int(end-start))
print "# Unique subreddit users found: %d" % len(s.authors)

session = Session()

# looks like it takes about 2 seconds every 25 comments. Again, makes sense, 
# and I don't think we'll be able to do any better than that.
# From 10 most recent posts: 25 users. Average=349, sdev=332
# 94 users ~ 50 minutes. 
# anticipate ~ 23 hours for 2605 users.

# Let's store all of our users FIRST. Then get their comments respectfully. Finding all these users only took 30 min. Getting all their comments should take at least a day. This way we can pick up where we left off.

# These lines commented out because we've already go our users stored.
#for username, user in s.authors.iteritems():
    #print "Getting %s's comments" % username
#    dbU = User(username) # store user in database
#    session.add(dbU)
#    session.commit()
    
#for username, user in s.authors.iteritems():

# This query is mad slwo. Let's use minus instead.
# session.query(User.username).filter(~exists().where(User.username==Comment.author)).all()

from sqlalchemy import distinct
allusers = session.query(User.username)
scraped = session.query(distinct(Comment.author)).all()
unscraped = [user for user in allusers if user not in scraped]

r=praw.Reddit(user_agent="/u/shaggorama prototype scraper")
for username in unscraped:
    start = time.time()           
#    comments = user.get_comments(limit=None)
    try:
        comments = r.get_redditor(username).get_comments(limit=None, url_data={'limit':100})
    except:
        print "Error received getting comments for username <%s>. Waiting 30s" % username
        time.sleep(30)        
        try:
            comments = r.get_redditor(username).get_comments(limit=None, url_data={'limit':100})
        except:
            print "fool me once shame on you. Fool me twice, shame on me. Looks like this user doesn't exist."
            print "Should flag this user somehow, but for the time being we'll just skip him."
            print "This of course means if we try to pick up where we left off later we'll run into all these users, but oh well."
            continue
    lc = 0
    try:
        for c in comments:
            lc +=1
            comment = Comment(c)
            try:                    
                session.add(comment)
                session.commit()
            except:
                session=Session()
    except:
        pass                
    end = time.time()
    gm_end = time.gmtime(end)
    print "        %d:%d - %s: %d comments downloaded in %d seconds." % (gm_end.tm_hour, gm_end.tm_min, username, lc, int(end-start))

print "Total Elapsed time:", time.time() - starttime
