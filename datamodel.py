from database import *
from sqlalchemy import Table, Column, Boolean, Float, Integer, String, Unicode, DateTime, ForeignKey
from sqlalchemy.orm import relation,backref
import datetime 

class User(Base):
    """
    Connects select fields of a praw.Redditor object to the db
    """
    __tablename__ = 'users'
    username = Column(String, primary_key=True)
    created_date = Column(DateTime)
    #last_scraped = Column(DateTime)
    
    def __init__(self,u): #,l=datetime.datetime.now()):
        self.username = u
        self.created_date = datetime.datetime.now() #This looks wierd to me, but it works... This should really be a database-side trigger, though.
        #self.last_scraped = l
    
class Comment(Base):
    """
    Connects select fields of a praw.Comment object to the db
    """

    __tablename__ = 'comments'
    comment_id      = Column(String, primary_key=True)
    subreddit_id    = Column(String)
    subreddit_name  = Column(String)
    comment_body    = Column(String)
    author          = Column(String)
    created_utc     = Column(Float)  
    link_id         = Column(String)
    link_title      = Column(String)
    ups             = Column(Integer)
    downs           = Column(Integer)
    parent_id       =  Column(String)
   
    def __init__(self, comment):
        self.comment_id     = comment.name
        self.subreddit_id   = comment.subreddit_id
        self.subreddit_name = comment.subreddit.display_name
        self.comment_body   = comment.body
        self.author         = comment.author.name
        self.created_utc    = comment.created_utc
        self.link_id        = comment.link_id
        self.link_title     = comment.link_title
        self.ups            = comment.ups
        self.downs          = comment.downs
        self.parent_id      = comment.parent_id
        self.score          = self.ups - self.downs
    
