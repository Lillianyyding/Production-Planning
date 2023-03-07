#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 09:39:50 2022

@author: lillianding
"""

#!/usr/bin/env python
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
import copy
import datetime
import collections
pd.options.mode.chained_assignment = None  # default='warn'



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
# In[2]:
SMART = pd.read_excel('Smart Factory.xlsx')
SMART = SMART.drop_duplicates(subset=['Slot #','Module #'])
SMART['Revised Complete'] = pd.to_datetime(SMART['Revised Complete'],errors='ignore')
SMART['Actual Complete'] = pd.to_datetime(SMART['Actual Complete'],errors='ignore')
SMART['Revised Start Build'] = pd.to_datetime(SMART['Revised Start Build'],errors='ignore')
SMART['Revised Test Start'] = pd.to_datetime(SMART['Revised Test Start'],errors='ignore')
SMART['Actual Test Start'] = pd.to_datetime(SMART['Actual Test Start'],errors='ignore')
SMART['Revised Test Complete'] = pd.to_datetime(SMART['Revised Test Complete'],errors='ignore')
SMART['EOP Plan'] = pd.to_datetime(SMART['EOP Plan'],errors='ignore')
SMART['EOP Revised'] = pd.to_datetime(SMART['EOP Revised'],errors='ignore')
# In[3]:

DATA = {
    'WF Slot #':[],'Slot #':[],'WF Module':[],'Module':[],'WF Hol,Wkd,Revised Start':[],'Hol,Wkd,Revised Start':[],
    'WF Planned Build Start':[],'Planned Build Start':[],'WF Planned Test Start':[],'Planned Test Start':[],
    'WF Comp Date Revised EOP':[],'Comp Date Revised EOP':[],'WF Planned EOP':[],'Planned EOP':[]}
for index,item in SMART.iterrows():
    if pd.isnull(item['Planned Start Build']):
        continue
    if 'WR' in item['Module #']:
        a = 'Std '
    else:
        a = 'NPI '
    if 'INTC' in item['Module #'] or 'CLNR' in item['Module #'] or 'Cleaner' in item['Product Name'] or 'CLEANER' in item['Product Name']:
        b = 'Clnr'
    else:
        b = 'Pol'
    module = a + b
    pbs2 = item['Planned Start Build']
    if pd.isnull(item['Actual Start Build']) and pd.isnull(item['Revised Start Build']):
        rbs2 = item['Planned Start Build']
    elif pd.isnull(item['Actual Start Build']) == False:
        rbs2 = item['Actual Start Build']
    else:
        rbs2 = item['Revised Start Build']
    if pd.isnull(item['Actual Test Start']) == False:
        pts2 = item['Actual Test Start']
    elif pd.isnull(item['Revised Test Start']) == False:
        pts2 = item['Revised Test Start']
    else:
        pts2 = None
    pEOP2 = item['EOP Plan']
    rEOP2 = item['EOP Revised']
    if item['Slot #'] not in list(waterfall['Slot #']):
        rbs1,pbs1,pts1,rEOP1,pEOP1 = None,None,None,None,None
        #print(item['Slot #'])
        DATA['WF Slot #'].append(None)
        DATA['WF Module'].append(None)
        DATA['WF Hol,Wkd,Revised Start'].append(rbs1)
        DATA['WF Planned Build Start'].append(pbs1)
        DATA['WF Comp Date Revised EOP'].append(rEOP1)
        DATA['WF Planned EOP'].append(pEOP1)
        DATA['Slot #'].append(item['Slot #'])
        DATA['Module'].append(module)
        DATA['Hol,Wkd,Revised Start'].append(rbs2)
        DATA['Planned Build Start'].append(pbs2)
        DATA['Comp Date Revised EOP'].append(rEOP2)
        DATA['Planned EOP'].append(pEOP2)
        DATA['WF Planned Test Start'].append(pts1)
        DATA['Planned Test Start'].append(pts2)
    Append = False
    for IDX,IT in waterfall.iterrows():
        if IT['Slot #'] == item['Slot #']:
            slotN = IT['Slot #']
            moduleN = IT['Module']
            rbs1,pbs1,pts1,rEOP1,pEOP1 = IT['Hol,Wkd,Revised Start'],IT['Planned Build Start'],IT['Planned Test Start'],IT['Comp Date Revised EOP'],IT['Planned EOP']
            if pd.isnull(item['Revised Test Complete']):
                if pd.isnull(pts2):
                    if rbs1 != rbs2 or pbs1 != pbs2:
                        Append = True
                else:
                    if rbs1 != rbs2 or pbs1 != pbs2 or pts1 != pts2:
                        Append = True
            else:
                if rbs1 != rbs2 or pbs1 != pbs2 or pts1 != pts2 or rEOP1 != rEOP2 or pEOP1 != pEOP2:
                    Append = True
    if Append == True:
        DATA['WF Slot #'].append(slotN)
        DATA['WF Module'].append(moduleN)
        DATA['WF Hol,Wkd,Revised Start'].append(rbs1)
        DATA['WF Planned Build Start'].append(pbs1)
        DATA['WF Comp Date Revised EOP'].append(rEOP1)
        DATA['WF Planned EOP'].append(pEOP1)
        DATA['Slot #'].append(item['Slot #'])
        DATA['Module'].append(module)
        DATA['Hol,Wkd,Revised Start'].append(rbs2)
        DATA['Planned Build Start'].append(pbs2)
        DATA['Comp Date Revised EOP'].append(rEOP2)
        DATA['Planned EOP'].append(pEOP2)
        DATA['WF Planned Test Start'].append(pts1)
        DATA['Planned Test Start'].append(pts2)          
# In[4]:
df = pd.DataFrame.from_dict(DATA)
for key in ['WF Hol,Wkd,Revised Start','Hol,Wkd,Revised Start','WF Planned Build Start','Planned Build Start','WF Planned Test Start','Planned Test Start',
    'WF Comp Date Revised EOP','Comp Date Revised EOP','WF Planned EOP','Planned EOP']:
    df[key] = pd.to_datetime(df[key],errors='ignore')

# In[5]:

for IDX,IT in df.iterrows():
    rbs1,pbs1,pts1,rEOP1,pEOP1 = IT['WF Hol,Wkd,Revised Start'],IT['WF Planned Build Start'],IT['WF Planned Test Start'],IT['WF Comp Date Revised EOP'],IT['WF Planned EOP']
    rbs2,pbs2,pts2,rEOP2,pEOP2 = IT['Hol,Wkd,Revised Start'],IT['Planned Build Start'],IT['Planned Test Start'],IT['Comp Date Revised EOP'],IT['Planned EOP']
    if rbs1 == rbs2 and pbs1 == pbs2 and pts1 == pts2 and rEOP1 == rEOP2 and pEOP1 == pEOP2:
        print(True)
        df.drop(IDX)

# In[6]:
df.to_csv('Progress_Revised.csv')



