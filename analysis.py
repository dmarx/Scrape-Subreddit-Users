import database as db
from datamodel import *
import time
import datetime as dt
import pylab as pl
import pandas as pd
import numpy as np

s = db.Session()
data = s.query(Comment.author, Comment.comment_id, Comment.created_utc).all()

author        = [a for a,b,c in data]
comment_id    = [b for a,b,c in data]
timestamps    = [time.gmtime(c) for a,b,c in data]
created_dates = [dt.datetime(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec) for t in timestamps]

df = pd.DataFrame({'author':author, 'comment_id':comment_id}, index=created_dates)

# This gives us the total comments by hour. I want this normalized to percent of total.
# ... actually, if I use cosine similarity for clustering, it shouldn't make a difference.
grouped = df.groupby(['author', lambda x: x.hour]).agg(len)
grid    = grouped.unstack()

pl.plot(grid.T)
pl.show()


# Let's add some more features and break it out by day of week

# switching around lambdas would probably simplify unstacking
# can probably change .agg(len) to .count()
grouped2 = df.groupby(['author', lambda x: x.dayofweek, lambda x:x.hour]).agg(len)
grid2 = grouped2.unstack(1).unstack()
grid2 = grid2.fillna(0) # mainly for PCA, but can't hurt.
pl.plot(grid2.T)
pl.show


# pca
from sklearn.decomposition import PCA
pca = PCA(n_components=2)
pca.fit(grid2)
grid2_pca = pca.transform(grid2)
pl.scatter(grid2_pca.T[0], grid2_pca.T[1])
pl.show()

#filter on best data
filtered = grid2[grid2.T.sum()>900]
pca.fit(filtered)
f_pca = pca.transform(filtered)

pl.scatter(f_pca.T[0],f_pca.T[1])
pl.show()

# An attempt at spectral clustering. Doesn't really show anythign on the plot, anyway
from sklearn.clustering import SpectralClustering
spec = SpectralClustering(n_clusters=2)
spec.fit(grid2)
colors = np.array([x for x in 'bgrcmykbgrcmykbgrcmykbgrcmyk'])
colors = np.hstack([colors] * 20)
col = colors[spec.labels_.astype(np.int)].tolist()
x,y = grid_pca.T[0], grid_pca.T[1]
pl.scatter(x,y,color=col)





## Don't really know anythign about ward hierarchical clustering,
## but this works as a proof of concept.
## For visualization purposes, we could probably get away 
## with some PCA here as well, maybe make this 3D.
#from sklearn.cluster import Ward
#ward  = Ward(n_clusters=10).fit(grid)
#label = ward.labels_
#
#for l in np.unique(label):
#    pl.plot(grid[label==l].T, color=plt.cm.jet(np.float(l) / np.max(label + 1)))
