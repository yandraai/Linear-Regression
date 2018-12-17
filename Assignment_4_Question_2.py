
# coding: utf-8

# In[39]:


import os

#os.environ["PATH"] += os.pathsep + 'C:\\Users\\yandra\\Anaconda3\\Library\\bin\\graphviz'

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import transforms
from io import StringIO
from pandas import ExcelWriter
from pandas import ExcelFile
import seaborn as sns
import pydotplus
from IPython.display import Image
from sklearn.cluster import KMeans
from math import log
import numpy as np



from sklearn.metrics import silhouette_samples, silhouette_score

from sklearn.cluster import AgglomerativeClustering

import matplotlib.cm as cm
import scipy as sc
from scipy.cluster import hierarchy
from scipy.cluster.hierarchy import fcluster


# In[40]:


File = 'C:\\Users\\yandr\\OneDrive\\Desktop\\IDA\\Assignments\\four\\HW4GaussianClustersData.csv'

df1 = pd.read_csv(File)
 
print("Column headings:")
print(df1.columns)
df1.shape


# In[41]:


df = pd.DataFrame(dict(X=df1['X'], Y=df1['Y']))
plt.figure(figsize=(10,5))
#sns.lmplot('X', 'Y', data=df,fit_reg=False)
plt.scatter(df['X'],df['Y'], s=20, cmap='viridis');


# In[42]:


X_set=df.values[:,0:2]
#Y_set=df.values[:,1:2]
X_set


# In[43]:


kmeans=[]
sse=[]
bic=[]

def km(n):
    k=KMeans(n_clusters=n, random_state=0).fit(X_set)
    kmeans.append(k)
    sse_1=k.inertia_
    sse.append(sse_1) 
    bic.append(6600*log(sse_1/6600,2)+log(6600,2)*n*(3))

km(3)
km(5)
km(7)
km(9)
km(11)
km(13)
km(15)
km(17)
km(19)
    


# In[44]:


y_kmeans = kmeans[4].predict(X_set)
plt.figure(figsize=(16,6))
plt.scatter(X_set[:, 0], X_set[:, 1], c=y_kmeans, s=20, cmap='viridis')
centers = kmeans[4].cluster_centers_
plt.scatter(centers[:, 0], centers[:, 1], c='black', s=120, alpha=0.5);


# In[45]:


sse,bic


# In[46]:


f,(ax1,ax2)=plt.subplots(1,2,figsize=(16,4))

x=[3, 5, 7, 9, 11, 13, 15, 17,19]

plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.4, hspace=None)

ax1.plot( x,sse, marker='o', markerfacecolor='black', markersize=12, color='red', linewidth=1 , label="Recall before partition")

ax2.plot( x,bic, marker='o', markerfacecolor='black', markersize=12, color='red', linewidth=1 , label="Recall before partition")
plt.setp([ax1,ax2],xticks=x)
ax1.set_title('SSE Vs Clusters')
ax2.set_title('BIC Vs Clusters')
#plt.xticks(x,x)
plt.show()
#plt.xticks(x,x)


# In[47]:


silhouette_avg = silhouette_score(X_set, y_kmeans)
print("For n_clusters =", 11,
          "The average silhouette_score is :", silhouette_avg)


# In[48]:


sample_silhouette_values = silhouette_samples(X_set, y_kmeans)
sample_silhouette_values,len(sample_silhouette_values)


# In[51]:


y_lower =10
fig, (ax1,ax2) = plt.subplots(1, 2,figsize=(17,5))
for i in range(11):
    i_cluster_values=sample_silhouette_values[y_kmeans==i]
    i_cluster_values.sort()
    size_cluster_i = i_cluster_values.shape[0]
    y_upper = y_lower + size_cluster_i
    color = cm.nipy_spectral(float(i) / 11)
    ax1.fill_betweenx(np.arange(y_lower, y_upper),
                          0, i_cluster_values,
                          facecolor=color, edgecolor=color, alpha=0.7)
    ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))
    y_lower = y_upper + 10  # 10 for the 0 samples
    ax1.set_title("The silhouette plot for the various clusters.")
    ax1.set_xlabel("The silhouette coefficient values")
    ax1.set_ylabel("Cluster label")
    ax1.axvline(x=silhouette_avg, color="red", linestyle="--")
    ax1.set_yticks([])  # Clear the yaxis labels / ticks
    ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])
    
    
    colors = cm.nipy_spectral(y_kmeans.astype(float) / 11)
    ax2.scatter(X_set[:, 0], X_set[:, 1], marker='.', s=30, lw=0, alpha=0.7,
                c=colors, edgecolor='k')
    centers = kmeans[4].cluster_centers_
    # Draw white circles at cluster centers
    ax2.scatter(centers[:, 0], centers[:, 1], marker='o',
                c="black", alpha=1, s=200, edgecolor='k')
    centers = kmeans[4].cluster_centers_


# In[53]:


z=sc.cluster.hierarchy.linkage(X_set, method='single', metric='euclidean')


# In[58]:


plt.figure(figsize=(20,10))
plt.plot([0,100000],[3.2,3.2],'r')
r=sc.cluster.hierarchy.dendrogram(z,no_plot=False)


# In[64]:


fc=fcluster(z,3.2,criterion='distance')
plt.figure(figsize=(20,10))
#print(fc)
df['cluster']=fc
plt.scatter(df['X'],df['Y'],c=fc)
values, counts = np.unique(fc, return_counts=True)
print("Number of Data points in each cluster ",counts)
print("Cluster Number                        ",values)

