import praw
import database as db
from datamodel import *

_ua = "/u/shaggorama prototype scraper"
_targetsub = 'washingtondc'

class SubredditScraper(object):
    def __init__(self,ua=_ua):
        self.conn = praw.Reddit(user_agent=ua)
        self.authors={}        
    def scrapeSubredditUsers(self, sub=_targetsub, nposts=100):
        
        r = self.conn
        subreddit = r.get_subreddit(sub)
        posts     = subreddit.get_new_by_date(limit=None, url_data={'limit':100})

        n=0
        for p in posts:
            n+=1
            comments = p.all_comments_flat
            print "Scraped %d posts" % n
            lc = len(comments)
            nc = 0
            for c in comments:
                nc +=1
                #print "%d of %d comments scraped" % (nc, lc)
                try:
                    a = c.author
                    self.authors[a.name] = a
                except:
                    break
            if n >= nposts:
                break
