#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import copy
import datetime
import collections
pd.options.mode.chained_assignment = None  # default='warn'


# In[2]:


#waterfall = pd.read_excel('Waterfall Input.xlsx')
MPP = pd.read_csv('MPP File.csv')
MPP = MPP[MPP['Build BU Name'] == 'D9']
MPP = MPP[MPP['EOP Fiscal Quarter'] >= '2021Q4']
MPP = MPP[MPP['Plant'] == 4070]
MPP = MPP.drop_duplicates(subset=['Machine #'])
MPP['Machine #'] = MPP['Machine #']
MPP['SOP Actual'] = pd.to_datetime(MPP['SOP Actual'],errors='ignore')
MPP = MPP.set_index('Machine #')
#MPP['Location'][900886]


# In[3]:


waterfall = pd.read_excel('Waterfall Input.xlsx')
Column_Name = waterfall.loc[5]
waterfall = waterfall.iloc[6:,1:]
for c in Column_Name[7:13]:
    #print(c)
    waterfall[c] = pd.to_datetime(waterfall[c],format='%Y-%m-%d',errors='ignore')
    #print()
for c in Column_Name[13:17]:
    #print(c)
    waterfall[c] = pd.to_datetime(waterfall[c],format='%Y-%m-%d',errors='ignore')
waterfall = waterfall.loc[pd.isnull(waterfall['Slot #']) == False]


# In[4]:


New_Add = []
Miss_Out = []


# In[5]:

O = list(set(waterfall['Slot #'].to_list()))
N = MPP.index.tolist()
Original = []
New = []
for item in O:
    Original.append(str(item))
for item in N:
    New.append(str(item))


# In[6]:
#--- not in Original But not in New
for i in Original:
    if i not in New:
        Miss_Out.append(i)
#print(Miss_Out)
#--- not in New But not in Original
for i in New:
    if i not in Original:
        New_Add.append(i)


# In[ ]:


MPPcopy = MPP[MPP.index.isin(New_Add)]


# In[7]:


mx = max(len(New_Add),len(Miss_Out))
if len(New_Add) == mx:
    Miss_Out += [np.nan for i in range(abs(len(New_Add) - len(Miss_Out)))]
else:
    New_Add += [np.nan for i in range(abs(len(New_Add) - len(Miss_Out)))]                                   


# In[8]:


data = {'Miss Out': Miss_Out, 'New_Add': New_Add}


# In[9]:


df = pd.DataFrame.from_dict(data)


# In[10]:


df.to_csv('MPP_Miss_Add.csv')


# In[20]:


MPPcopy.to_csv('MPP_New_Add_Details.csv')

