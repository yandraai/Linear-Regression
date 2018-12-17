
# coding: utf-8

# In[1]:


import pandas as pd
import seaborn as sns
import statsmodels.formula.api as smf
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.regression.linear_model import OLS
from statsmodels.tools import add_constant
from sklearn import metrics
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


File = 'C:\\Users\\yandr\\OneDrive\\Desktop\\IDA\\Assignments\\four\\winequality-white.csv'

df = pd.read_csv(File,sep=';')
print("Column headings:")
print(df.columns)

df.shape


# In[4]:


#Initializing the Variables
lmwhite=[]
r2_value=[]
aic_value=[]
best_aic=[999999999999]
r2=[]
aic=[]
count=0
feature=""
flag='T'
counter=0
i_vector=[]
i_vec=[]
bestlm=[]

# Iterating through the combination of features

while(count<10):    
    print(count+1,"- feature Regression Models","\n")
    count=count+1
    counter=0
    i_vector=[]
    aic_value=[]  
    lmwhite=[]
    for i in df.columns:
        if i=="quality" or feature.find(i)>0:
            continue;
        if feature=="" :
            lmwhite_dummy=smf.ols(formula='quality~'+ i,data=df).fit()
        else :
            lmwhite_dummy=smf.ols(formula='quality~ '+feature+"+"+ i ,data=df).fit()
        i_vector.append(feature+ "+"+i)    
        lmwhite.append(lmwhite_dummy)
        r2_value_dummy=(lmwhite_dummy.rsquared)
        r2_value.append(r2_value_dummy)
        aic_value_dummy=(lmwhite_dummy.aic)
        aic_value.append(aic_value_dummy)
        print("Model:: ","Feature:",(feature+ "+"+i).strip("+"),"R2_Value:",
              round(r2_value_dummy,4),"AIC_Value:",round(aic_value_dummy,6),"\n") 
    
    i_vec.append(i_vector)
    aic.append(aic_value)
    r2.append(r2_value)
    feature_num = r2_value.index(max(r2_value))
    feature=i_vector[feature_num]
    print("Best Feature with highest r2 value:",feature.strip("+"),"R2_Value : ",
          round(r2_value[feature_num],4),"AIC_Value:",round(aic_value[feature_num],6),"\n")
    r2_value=[]
    best_aic.append(aic_value[feature_num])  
    bestlm.append(lmwhite[feature_num])
    
    # Stopping Condition
    for j in aic_value:
        if j>=best_aic[-2]:
            counter=counter+1  
        if counter==len(aic_value)-1:
            print("hello")
    


# In[5]:


bestlm[7].summary(),bestlm[7].pvalues


# In[6]:


File = 'C:\\Users\\yandr\\OneDrive\\Desktop\\IDA\\Assignments\\four\\featur.xlsx'
File1 = 'C:\\Users\\yandr\\OneDrive\\Desktop\\IDA\\Assignments\\four\\Y_AK.xlsx'
X_Val=pd.read_excel(File)
Y_Val=pd.read_excel(File1)
Y_Val


# In[9]:


df_white = pd.DataFrame(data=df,columns=df.columns)
X=df_white.values[:,0:11]
Y=df_white.values[:,11]
X


# In[12]:


lmwhite

pred=bestlm[7].predict(X_Val)
error= abs(pred-Y)

for index,i in enumerate(error):
    #print(index,i)
    if abs(i) >= 3.225:
        print(index)

dfsds=pd.DataFrame(error)
dfsds.to_excel('C:\\Users\\yandr\\OneDrive\\Desktop\\IDA\\Assignments\\four\\error1.xls', header=False, index=False)

dfsds1=pd.DataFrame(pred)
dfsds1.to_excel('C:\\Users\\yandr\\OneDrive\\Desktop\\IDA\\Assignments\\four\\pred1.xls', header=False, index=False)

