#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 12:03:08 2021

@author: lillianding
"""

#!/usr/bin/env python
# coding: utf-8

# In[261]:


import pandas as pd
import numpy as np
import copy
import datetime
import collections
import time


# In[145]:


def CountDays(Start,End):
    day = 0
    while Start < End:
        if Start not in Holidays_And_Weekends:
            day += 1
        Start += datetime.timedelta(days=1)
    return day
# In[146]:


class OrderAndModule:
    Number_Of_Order_And_Module = 0
    Defualt_Kit_Days = 4
    Defualt_Int_Days = 8
    Defualt_Test_Days = 7
    Defualt_Clean_Days = 2
    Priority = []
    def __init__(self, Customer, Slot_No, Module, Planned_EOP, Revised_EOP, Revised_Start, Planned_Build_Start, Planned_Test_Start, Ship_Revised):
        #Need to read the Slot#, Module type, planned_EOP, etc. information from the MPP file
        if type(Ship_Revised) == str and Ship_Revised[0] == '2':
            Ship_Revised = datetime.datetime.strptime(Ship_Revised,'%Y-%m-%d')
        self.Customer = Customer # data type: str
        self.Slot_No = Slot_No # data type: int
        self.Module = Module # data type: str
        self.Planned_EOP = Planned_EOP # Timestamp
        self.Revised_Start = Revised_Start # Timestamp
        self.Planned_Build_Start = Planned_Build_Start # TimeStamp
        self.Planned_Test_Start = Planned_Test_Start # TimeStamp
        self.Revised_EOP = Revised_EOP # TimeStamp
        if pd.isnull(Ship_Revised) == False and type(Ship_Revised) == datetime.datetime:
            self.EOP_DDD = Ship_Revised - datetime.timedelta(days=5) # TimeStamp
        self.Kit_Days = OrderAndModule.Defualt_Kit_Days # data type: str
        self.Int_Days = OrderAndModule.Defualt_Int_Days # data type: str
        self.Test_Days = OrderAndModule.Defualt_Test_Days # data type: str
        #self.EOP_TO_Cust_Commit_Days = (self.EOP_DDD - Revised_EOP).days #- Holidays
        if 'NPI' in  Module:
            self.Estimated_Start = self.Planned_EOP - datetime.timedelta(days=80)
        else:
            self.Estimated_Start = self.Planned_EOP - datetime.timedelta(days=20)
        OrderAndModule.AddOrderAndModule()
        OrderAndModule.Priority.append((self.Estimated_Start,self.Slot_No,self.Module))
    # Classmethod   
    @classmethod
    def NumberOfOrderAndModule(cls):
        return cls.Number_Of_Order_And_Module
    @classmethod
    def AddOrderAndModule(cls):
        cls.Number_Of_Order_And_Module += 1
        
    @classmethod
    def DeleteOrderAndModule(cls):
        cls.Number_Of_Order_And_Module -= 1
    
    # Delete an order and module accidentally added
    
    
    #Modify Object Feature Values
    # Syntax Example: ChangeIntDays(Order1,9) We've changed the integration day for order1 from 8 days to 9 days
    def ChangeIntDays(self,New_Int_Days):
        self.Int_Days = New_Int_Days
    def ChangeTestDays(self,New_Test_Days):
        self.Test_Days = New_Test_Days
    def ChangeKitDays(self, New_Kit_Days):
        self.Kit_Days = New_Kit_Days
    def ChangePlannedEOP(self, New_Planned_EOP):
        OrderAndModule.Priority.remove((self.Planned_EOP,self.Slot_No,self.Module))
        self.Planned_EOP = New_Planned_EOP
        if 'NPI' in  Module:
            self.Estimated_Start = self.Planned_EOP - datetime.timedelta(days=70)
        else:
            self.Estimated_Start = self.Planned_EOP - datetime.timedelta(days=20)
        OrderAndModule.AddOrderAndModule()
        OrderAndModule.Priority.append((self.Planned_EOP,self.Slot_No,self.Module))
    def ChangePlannedBuildStart(self, New):
        self.Planned_Build_Start = New
    def ChangeRevisedStart(self, New):
        self.Revised_Start = New
    def ChangePlannedTestStart(self, New):
        self.Planned_Test_Start = New
    # Get Object Feature
    def GetIntDays(self):
        return self.Int_Days
    def GetTestDays(self):
        return self.Test_Days
    def GetIntDays(self):
        return self.Kit_Days
    def GetPlannedEOP(self):
        return self.Planned_EOP
    def GetPlannedTestStart(self):
        return self.Planned_Build_Start
    def GetRevisedStart(self):
        return self.Revised_Start
    def GetPlannedTestStart(self):
        return self.Planned_Test_Start
    def GetDDDEOP(self):
        return self.EOP_DDD
    def GetEOPTOCustCommitDays(self):
        return self.EOP_TO_Cust_Commit_Days
    # Get and print all features in the object
    def GetAll(self):
#         print(self.Customer,
#         self.Slot_No,
#         self.Module,
#         self.Planned_EOP,
#         self.Revised_Start
#         self.Planned_Build_Start,
#         self.Planned_Test_Start,
#         self.Revised_EOP,
#         self.EOP_DDD,
#         self.Kit_Days,
#         OrderAndModule.Defualt_Int_Days,
#         self.Test_Days,
#         self.EOP_TO_Cust_Commit_Days)
        return self.Customer,
        self.Slot_No,
        self.Module,
        self.Planned_EOP,
        self.Revised_Start,
        self.Planned_Build_Start,
        self.Planned_Test_Start,
        self.Revised_EOP,
        self.EOP_DDD,
        self.Kit_Days,
        OrderAndModule.Defualt_Int_Days,
        self.Test_Days,
        self.EOP_TO_Cust_Commit_Days, self.Estimated_Start


# In[147]:


# Function: Re-Value Waterfall and Assign objects in OrderAndModule Class
def GenerateOrders(waterfall):
    ORDER = {}
    OrderAndModule.Priority = [] #initialize Class
    #Customer, Slot_No, Module, Planned_EOP, Revised_EOP,self.Revised_Start, Planned_Build_Start, Planned_Test_Start, Ship_Revised)
    for index, item in waterfall.iterrows():
        #---filter data start
        if type(item['Slot #']) != int:
            continue
        if  pd.isnull(item['Comp Date Revised EOP']) or item['Comp Date Revised EOP'] >= Original_End_Time:
            Update_List.append((item['Slot #'],item['Module']))
        #---add object to OrderAndModule class
        #Customer, Slot_No, Module, Planned_EOP, Revised_EOP, Revised_Start, Planned_Build_Start, Planned_Test_Start, Ship_Revised)
        if pd.isnull(item['EOP DDD']) or item['EOP DDD'] == ' ':
            item['EOP DDD'] = item['BD Start date']
        ORDER[(item['Slot #'],item['Module'])] = OrderAndModule(item['Customer'],item['Slot #'],item['Module'],item['Planned EOP'],item['Comp Date Revised EOP'],item['Hol,Wkd,Revised Start'], item['Planned Build Start'],item['Planned Test Start'],item['Ship Revised'])
        ORDER[(item['Slot #'],item['Module'])].ChangeIntDays(item['Int'])
        ORDER[(item['Slot #'],item['Module'])].ChangeTestDays(item['Final Test'])
        cmp = False
        for a in item:
            if type(a) == str:
                if a == 'Comp Date':
                    cmp = True
                if 'Test' in a and cmp == True:
                    Update_List.append((item['Slot #'],item['Module']))
                    break
    return waterfall,ORDER



# In[148]:


# Initial Bays Capacity From DataFrame waterfall variable
def CalBaysCapacity(waterfall):
    Sttart = {}
    Int_Total = {}
    Int_Clnr = {}
    Int_Pol = {}
    Test_Total = {}
    Test_Clnr = {}
    Test_Pol = {}
    Kit_Total = {}
    Start = {}
    NPI_Total = {}
    NPI = waterfall.loc[waterfall['Module'].str.contains('NPI', na = False)]
    Pol = waterfall.loc[waterfall['Module'].str.contains('Pol', na = False)]
    Clnr = waterfall.loc[waterfall['Module'].str.contains('Clnr', na = False)]
    for t in Time_List_Index:
        temp1 = Clnr.loc[Clnr[t].str.contains('Int',na = False)]
        Int_Clnr[t]=[(item['Slot #'],item['Module'])for index, item in temp1.iloc[:,np.r_[0,3]].iterrows()]
        temp2 = Pol.loc[Pol[t].str.contains('Int',na = False)]
        Int_Pol[t]=[(item['Slot #'],item['Module'])for index, item in temp2.iloc[:,np.r_[0,3]].iterrows()]
        Int_Total[t] = Int_Clnr[t] + Int_Pol[t]
        temp3 = Clnr.loc[Clnr[t].str.contains('Test',na = False)]
        Test_Clnr[t]=[(item['Slot #'],item['Module'])for index, item in temp3.iloc[:,np.r_[0,3]].iterrows()]
        temp4 = Pol.loc[Pol[t].str.contains('Test',na = False)]
        Test_Pol[t]=[(item['Slot #'],item['Module'])for index, item in temp4.iloc[:,np.r_[0,3]].iterrows()]
        Test_Total[t] = Test_Clnr[t] + Test_Pol[t]
        temp5 = waterfall.loc[waterfall[t].str.contains('Kit',na = False)]  
        Kit_Total[t] = [(item['Slot #'],item['Module'])for index, item in temp5.iloc[:,np.r_[0,3]].iterrows()]
        temp6 = waterfall.loc[waterfall[t].str.contains('Int Start',na = False)] 
        Start[t] = [(item['Slot #'],item['Module'])for index, item in temp6.iloc[:,np.r_[0,3]].iterrows()]
        tempNPI = NPI.loc[NPI[t].str.contains('Int',na = False)]
        NPI_Total[t]=[(item['Slot #'],item['Module'])for index, item in tempNPI.iloc[:,np.r_[0,3]].iterrows()]
    return Int_Total,Int_Clnr,Int_Pol,Test_Total,Test_Clnr,Test_Pol,Kit_Total,Start,NPI_Total


# In[149]:


#update int and test days
def Update(w, ORDER, Slot_No, Module, Revised_Start, Int_Days, Test_Days):
    while Revised_Start in Holidays_And_Weekends:
        Revised_Start += datetime.timedelta(days=1)
    ORDER[(Slot_No, Module)].Int_Days = Int_Days
    ORDER[(Slot_No, Module)].Test_Days = Test_Days
    ORDER[(Slot_No, Module)].Revised_Start = Revised_Start
    w['Int'][(Slot_No, Module)] = Int_Days
    w['Final Test'][(Slot_No, Module)] = Test_Days
    w['Hol,Wkd,Revised Start'][(Slot_No, Module)] = Revised_Start
    #--- Update Kit Time
    #print('Kit')
    now =  Revised_Start
    Kit = True
    d = 1
    holiday = 0
    #print((Slot_No, Module),now)
    pre = now - datetime.timedelta(days=1)
    #print('Read',Slot_No, Module)
    while Kit == True:
        #print('pre',pre)
        #print(pre)
        if pre in Holidays_And_Weekends:
            pre -= datetime.timedelta(days=1)
            continue
        if pre > Time_List_Index[-1]:
            break
        if d >= 4:
            w[pre][(Slot_No, Module)] = 'Kit Start'
            Kit = False
            break
        #print(type(pre))
        w[pre][(Slot_No, Module)] = 'Kit'
        pre -= datetime.timedelta(days=1)
        d += 1
    t = Time_List_Index[0]
    #---make sure all the cells before kitting starts are None
    #print(pre)
    pre -= datetime.timedelta(days=1)
    while pre in Holidays_And_Weekends:
        pre -= datetime.timedelta(days=1)
    while t <= pre:
        #print(t)
        if t in Holidays_And_Weekends:
            t += datetime.timedelta(days=1)
            continue
        if now > Time_List_Index[-1]:
            break
        w[t][(Slot_No, Module)] = None
        t += datetime.timedelta(days=1)
    
    #--- Update Int Time
    Int = True
    now =  Revised_Start
    #print('Int')
    d = 1
    if now > Time_List_Index[-1]:
        return w,ORDER
    w[now][(Slot_No, Module)] = 'Int Start' #IMPORTANT Assume: the revised start day is not on Holiday or weekends
    while d < Int_Days and Int == True and now <= Time_List_Index[-1]:
        #print(now)
        now = now + datetime.timedelta(days=1)
        if now in Holidays_And_Weekends:
            holiday += 1
            continue
        if d >= Int_Days or now > Time_List_Index[-1]:
            Int = False
            break
        w[now][(Slot_No, Module)] = 'Int'
        d += 1
    #--- Update Test Time
    Test = True
    #print('Test')
    d = 1
    now = now + datetime.timedelta(days=1)
    while now in Holidays_And_Weekends:
        holiday += 1
        now = now + datetime.timedelta(days=1)
    if now > Time_List_Index[-1]:
        return w,ORDER
    w[now][(Slot_No, Module)] = 'Test Start'
    w['Planned Test Start'][(Slot_No, Module)] = now
    ORDER[(Slot_No, Module)].Planned_Test_Start = now
    while d < Test_Days and Test == True and now <= Time_List_Index[-1]:
        #print(now)
        now = now + datetime.timedelta(days=1)
        if now in Holidays_And_Weekends:
            holiday += 1
            continue
        if d >= Test_Days:
            Test = False
            break
        if now > Time_List_Index[-1]:
            return w,ORDER
        w[now][(Slot_No, Module)] = 'Test'
        d += 1
    #--- Find Revised_EOP
    now = now + datetime.timedelta(days=1)
    if now > Time_List_Index[-1]:
        return w,ORDER
    while now in Holidays_And_Weekends:
        holiday += 1
        now = now + datetime.timedelta(days=1)
    #print(now)
    if now > Time_List_Index[-1]:
        return w,ORDER
    w[now][(Slot_No, Module)] = np.nan # one day gap one day between Test Finish and revised EOP
    now = now + datetime.timedelta(days=1)
    if now > Time_List_Index[-1]:
        return w,ORDER
    while now in Holidays_And_Weekends:
        holiday += 1
        now = now + datetime.timedelta(days=1)
    #print(now)
    if now > Time_List_Index[-1]:
        return w,ORDER
    ORDER[(Slot_No, Module)].Revised_EOP = now
    w['Comp Date Revised EOP'][(Slot_No, Module)] = now
    w[now][(Slot_No, Module)] = 'Comp Date'
    #--- calculate building cycle
    #w['Build Cycle Time'][(Slot_No, Module)] = Int_Days + Test_Days
    
    #--- Get EOP to commit days
    if hasattr(ORDER[(Slot_No, Module)], 'EOP_DDD'):
        commit = (ORDER[(Slot_No, Module)].EOP_DDD - now).days - holiday
        w['EOP to Cust Commit Days'][(Slot_No, Module)] = commit
        ORDER[(Slot_No, Module)].EOP_TO_Cust_Commit_Days = commit
    #---Make sure nan after Revised_EOP
    now = now + datetime.timedelta(days=1) # now is one day after revised EOP
    if now > Time_List_Index[-1]:
        return w,ORDER
    while now < Time_List_Index[-1]:
        #print(now)
        if now in Holidays_And_Weekends:
            now = now + datetime.timedelta(days=1)
            continue
        w[now][(Slot_No, Module)] = np.nan
        now = now + datetime.timedelta(days=1)
    return w,ORDER


# In[187]:


def ReflowTestOnly(w, ORDER, Slot_No, Module, Test_Start, Int_Days, Test_Days):
    #print('Test Start',Test_Start)
    #print(Int_Days)
    now = Test_Start
    '''
    Old_Start = ORDER[(Slot_No, Module)].Planned_Test_Start
    if pd.isnull(Old_Start) or now < Old_Start :
        Old_Start =  w['Hol,Wkd,Revised Start'][(Slot_No, Module)]
        d = 1
        while d <= Int_Days :
            if Old_Start in Holidays_And_Weekends:
                Old_Start += datetime.timedelta(days=1)
                continue
            #print(Old_Start)
            Old_Start += datetime.timedelta(days=1)
            d += 1
    else: 
        d = 0
    '''
    Old_Start = ORDER[(Slot_No, Module)].Revised_Start
    
    #--- Build gaps between old start and new start
    t = Old_Start
    
    #print(Old_Start, Test_Start)
    count = 0
    tempd = Int_Days
    Int_Days = 0
    while t < Test_Start:
        #print(True, t, Test_Start)
        if t in Holidays_And_Weekends:
            t += datetime.timedelta(days=1)
            continue
        count += 1
        if Hold_Int == True:
            w[t][(Slot_No, Module)] = 'Int'
        else:
            #print(count)
            if count <= tempd:
                w[t][(Slot_No, Module)] = np.nan = 'Int'
            else:
                w[t][(Slot_No, Module)] = np.nan
        t += datetime.timedelta(days=1)
        Int_Days += 1
    if Hold_Int == True:
        w['Int'][(Slot_No, Module)] = Int_Days
        ORDER[(Slot_No, Module)].Int_Days = Int_Days
    #print(Old_Start, t, now)
    w[now][(Slot_No, Module)] = 'Test Start'
    w['Planned Test Start'][(Slot_No, Module)] = now
    ORDER[(Slot_No, Module)].Planned_Test_Start = now
    d = 1
    Test = True
    while d < Test_Days and Test == True and now <= Time_List_Index[-1]:
        #print(now)
        now = now + datetime.timedelta(days=1)
        if now in Holidays_And_Weekends:
            continue
        if d >= Test_Days:
            Test = False
            break
        if now > Time_List_Index[-1]:
            return w,ORDER
        w[now][(Slot_No, Module)] = 'Test'
        d += 1
    #--- Find Revised_EOP
    now = now + datetime.timedelta(days=1)
    if now > Time_List_Index[-1]:
        return w,ORDER
    while now in Holidays_And_Weekends:
        now = now + datetime.timedelta(days=1)
    #print(now)
    if now > Time_List_Index[-1]:
        return w,ORDER
    w[now][(Slot_No, Module)] = np.nan # gap one day between Test Finish and revised EOP
    now = now + datetime.timedelta(days=1)
    if now > Time_List_Index[-1]:
        return w,ORDER
    while now in Holidays_And_Weekends:
        now = now + datetime.timedelta(days=1)
    #print(now)
    if now > Time_List_Index[-1]:
        return w,ORDER
    ORDER[(Slot_No, Module)].Revised_EOP = now
    w['Comp Date Revised EOP'][(Slot_No, Module)] = now
    w[now][(Slot_No, Module)] = 'Comp Date'
    #--- calculate building cycle
    w['Build Cycle Time'][(Slot_No, Module)] = Int_Days + Test_Days
    #--- Get EOP to commit days
    holiday = 0
    for t in Holidays_And_Weekends:
        if t > ORDER[(Slot_No, Module)].Revised_Start:
            holiday += 1
        if t > now:
            break
    if hasattr(ORDER[(Slot_No, Module)], 'EOP_DDD'):
        commit = (ORDER[(Slot_No, Module)].EOP_DDD - now).days - holiday
        w['EOP to Cust Commit Days'][(Slot_No, Module)] = commit
        ORDER[(Slot_No, Module)].EOP_TO_Cust_Commit_Days = commit
    #---Make sure nan after Revised_EOP
    now = now + datetime.timedelta(days=1) # now is one day after revised EOP
    if now > Time_List_Index[-1]:
        return w,ORDER
    while now < Time_List_Index[-1]:
        #print(now)
        if now in Holidays_And_Weekends:
            now = now + datetime.timedelta(days=1)
            continue
        w[now][(Slot_No, Module)] = np.nan
        now = now + datetime.timedelta(days=1)
    return w,ORDER


# In[151]:


def CalBaysCapacity_oneday(waterfall,D):
    Sttart = {}
    Int_Total = {}
    Int_Clnr = {}
    Int_Pol = {}
    Test_Total = {}
    Test_Clnr = {}
    Test_Pol = {}
    Kit_Total = {}
    Start = {}
    NPI_Total = {}
    NPI = waterfall.loc[waterfall['Module'].str.contains('NPI', na = False)]
    Pol = waterfall.loc[waterfall['Module'].str.contains('Pol', na = False)]
    Clnr = waterfall.loc[waterfall['Module'].str.contains('Clnr', na = False)]
    for t in [D]:
        temp1 = Clnr.loc[Clnr[t].str.contains('Int',na = False)]
        Int_Clnr[t]=[(item['Slot #'],item['Module'])for index, item in temp1.iloc[:,np.r_[0,3]].iterrows()]
        temp2 = Pol.loc[Pol[t].str.contains('Int',na = False)]
        Int_Pol[t]=[(item['Slot #'],item['Module'])for index, item in temp2.iloc[:,np.r_[0,3]].iterrows()]
        Int_Total[t] = Int_Clnr[t] + Int_Pol[t]
        temp3 = Clnr.loc[Clnr[t].str.contains('Test',na = False)]
        Test_Clnr[t]=[(item['Slot #'],item['Module'])for index, item in temp3.iloc[:,np.r_[0,3]].iterrows()]
        temp4 = Pol.loc[Pol[t].str.contains('Test',na = False)]
        Test_Pol[t]=[(item['Slot #'],item['Module'])for index, item in temp4.iloc[:,np.r_[0,3]].iterrows()]
        Test_Total[t] = Test_Clnr[t] + Test_Pol[t]
        temp5 = waterfall.loc[waterfall[t].str.contains('Kit',na = False)]  
        Kit_Total[t] = [(item['Slot #'],item['Module'])for index, item in temp5.iloc[:,np.r_[0,3]].iterrows()]
        temp6 = waterfall.loc[waterfall[t].str.contains('Int Start',na = False)] 
        Start[t] = [(item['Slot #'],item['Module'])for index, item in temp6.iloc[:,np.r_[0,3]].iterrows()]
        tempNPI = NPI.loc[NPI[t].str.contains('Int',na = False)]
        NPI_Total[t]=[(item['Slot #'],item['Module'])for index, item in tempNPI.iloc[:,np.r_[0,3]].iterrows()]
    return Int_Total,Int_Clnr,Int_Pol,Test_Total,Test_Clnr,Test_Pol,Kit_Total,Start,NPI_Total


# In[152]:


def CheckBaysCapcity(w,D): # DataFrame and Now
    while D < Time_List_Index[-2]:
        Int_Total,Int_Clnr,Int_Pol,Test_Total,Test_Clnr,Test_Pol,Kit_Total,Start,NPI_Total = CalBaysCapacity_oneday(w,D)
        print('Check Capacity on', D)
        if D in Holidays_And_Weekends:
            D += datetime.timedelta(days=1)
            continue
        if Relow_Merlion == True:
            if len(NPI_Total[D]) > CP[('NPIInt',D)]:
                return D, 'NPIInt', NPI_Total[D]
        if len(Int_Total[D]) > CP[('Int',D)]:
            return D, 'Int',Int_Total[D]
        if len(Test_Pol[D]) > CP[('PolTest',D)]:
            return D, 'PolTest', Test_Pol_Total[D]
        if len(Test_Total[D]) > CP[('Test',D)]:
            return D, 'Test', Test_Total[D]
        D += datetime.timedelta(days=1)
    return True


# In[153]:


def CheckPriority(candidates):
    priorityID = sorted([ID[i] for i in candidates])
    priority = [IDInv[i] for i in priorityID]
    return priority


# In[183]:


# Reflow Rules
# if capacity exceeds on Day D, 
# Find find the No. of  overflow, 
# move the one(s) revised planned start day after D, check capacities start from D + 1
def Reflow(w,D, End_Time,ORDER):
    while D < End_Time:
        print('-----Reflow on', D)
        if D in Holidays_And_Weekends:
            D += datetime.timedelta(days=1)
            continue
        ANS = CheckBaysCapcity(w,D)
        if ANS == True:
            return w,ORDER
        D = ANS[0]
        Trigger = ANS[1]
        reflow_candidates = ANS[-1]
        # For example, we have 16 reflow_candidates
        # we only reflow the two who have the least two priorities
        reflow_priority = CheckPriority(reflow_candidates)[CP[(ANS[1],D)]:]
        # reflow the starting time after day D + 1
        #D += datetime.timedelta(days=1)
        reflow_d = D + datetime.timedelta(days=1)
        if reflow_d > Time_List_Index[-3]:
            return w, ORDER
        if D == End_Time:
            return w,ORDER
        print('Reflow Triggered Condition',Trigger) 
        #print(len(reflow_candidates))
        for candidate in reflow_priority: # reflow candidates on D + 1 sequentially
            #print(candidate)
            while reflow_d in Holidays_And_Weekends:
                reflow_d += datetime.timedelta(days=1)
            if Trigger in ['PolTest','Test']:
                #print(candidate)
                #print(ORDER[candidate].Int_Days)
                Int_Days, Test_Days = ORDER[candidate].Int_Days, ORDER[candidate].Test_Days
                w,ORDER = ReflowTestOnly(w, ORDER, candidate[0], candidate[1], reflow_d, Int_Days, Test_Days)
                if candidate == reflow_priority[0]:
                    D = ORDER[(candidate[0], candidate[1])].Revised_Start
            else:
                Int_Days, Test_Days = ORDER[candidate].Int_Days, ORDER[candidate].Test_Days
                w,ORDER = Update(w, ORDER, candidate[0], candidate[1], reflow_d, Int_Days, Test_Days)
            reflow_d += datetime.timedelta(days=1)
    return w, ORDER


# In[155]:


def highlight_cells(val):
    H1 =  'background-color: yellow;'
    H2 =  'background-color: navy;'
    H3 = 'background-color: tan;'
    H4 = 'background-color: grey;'
    H5 = 'background-color: yellowgreen;'
    H6 = 'background-color: firebrick;'
    H7 = 'background-color: cornflowerblue;'
    H8 = 'background-color: chocolate;'
    default = ''
    if val == 'Int':
        return H1
    if val == 'Final Test':
        return H2
    if val == 'Planned Test Start':
        return H7
    if val == 'Hol,Wkd,Revised Start':
        return H4
    if val == 'Comp Date Revised EOP':
        return H5
    if val == 'EOP DDD' or val == 'Ship Revised':
        return H8
    if val == 'BD Start date':
        return H6
    if 'Int' == val:
        return H1
    if 'Int Start' == val:
        return H1
    if 'Test' == val:
        return H2
    if 'Test Start' == val:
        return H2
    if 'Final Test' == val:
        return H2
    if 'Kit' == val:
        return H3
    if 'Kit Start' == val:
        return H3
    if val == 'Hol, Wkd':
        return H4
    if val == 'Comp Date':
        return H5
    if val == 'EOP':
        return H5
    return default


# ## Read and Preprocessing Data

# In[278]:


# Generate Holiday and Weekends list
starttime = time.time()
Update_List = []
Pre_Time_Num = 17
pd.options.mode.chained_assignment = None  # default='warn'
Holidays_And_Weekends = pd.date_range(start = '2021-10-03', periods = 400, freq='w').to_pydatetime().tolist()
Holidays_And_Weekends += [datetime.datetime(2021,11,25,0,0),datetime.datetime(2021,11,26,0,0),
                          datetime.datetime(2021,12,24,0,0),datetime.datetime(2021,12,25,0,0),
                          datetime.datetime(2021,12,31,0,0),datetime.datetime(2022,1,1,0,0),
                          datetime.datetime(2022,1,17,0,0),datetime.datetime(2022,2,21,0,0),
                          datetime.datetime(2022,5,30,0,0),datetime.datetime(2022,7,4,0,0),
                          datetime.datetime(2022,9,4,0,0),datetime.datetime(2022,11,25,0,0),
                          datetime.datetime(2022,11,26,0,0),datetime.datetime(2022,12,24,0,0),
                          datetime.datetime(2022,12,25,0,0),datetime.datetime(2022,12,31,0,0),
                          datetime.datetime(2023,1,1,0,0),
                          datetime.datetime(2023,1,17,0,0),datetime.datetime(2023,2,21,0,0),
                          datetime.datetime(2023,5,30,0,0),datetime.datetime(2023,7,4,0,0),
                          datetime.datetime(2023,9,4,0,0),datetime.datetime(2023,11,25,0,0),
                          datetime.datetime(2023,11,26,0,0),datetime.datetime(2023,12,24,0,0),
                          datetime.datetime(2023,12,25,0,0),datetime.datetime(2023,12,31,0,0)]
# Planning End Time
dataf = pd.read_excel('Reflow Input.xlsx')
if pd.isnull(dataf['Extend Time To:'][1]) == False:
    Planning_End_Time = dataf['Extend Time To:'][1]
else:
    Planning_End_Time = '2023-12-31'
if dataf['Reflow Merlion'][1] == 1:
    Relow_Merlion = True
else:
    Relow_Merlion = False
if pd.isnull(dataf['Saved as'][1]):
    File_Name = 'Reflow Output'
else:
    File_Name = dataf['Saved as'][1]
if pd.isnull(dataf['Hold in Integration Bay'][1]):
    Hold_Int = True
else:
    Hold_Int = False


Time_List_Index = pd.date_range(start = '2021-9-27', end = Planning_End_Time, freq='d').to_pydatetime().tolist()
# read the old waterfall plan
#MPP = pd.read_csv('MPP Input.csv',engine='python')
waterfall = pd.read_excel('Waterfall Input.xlsx')

Column_Name = waterfall.loc[5]
Original_End_Time = datetime.datetime.strptime(Column_Name[-1],'%Y-%m-%d')
Push_Date = datetime.datetime.strptime(Column_Name[-1], '%Y-%m-%d')
for t in Time_List_Index:
    if t > Push_Date:
        if t in Holidays_And_Weekends:
            waterfall[t] = 'Hol, Wkd'
            continue
        waterfall[t] = ''
waterfall = waterfall.iloc[6:,1:]

for c in Column_Name[8:18]:
    #print(c)
    waterfall[c] = pd.to_datetime(waterfall[c],format='%Y-%m-%d',errors='ignore')


waterfall,ORDER = GenerateOrders(waterfall)
w1 = waterfall.set_index([waterfall['Slot #'],waterfall['Module']])
#---Extend time list
for key in Update_List:
    if ORDER[key].Revised_Start < Time_List_Index[0] or ORDER[key].Planned_EOP == np.nan:
        continue
    w1,ORDER = Update(w1, ORDER, key[0], key[1], ORDER[key].Revised_Start, ORDER[key].Int_Days, ORDER[key].Test_Days)


# In[279]:


#---Reflow Input
new_start_day = []
for index, item in dataf.iterrows():
    if index == 0:
        continue
    #print( Slot_No, Module)
    Slot_No,Module = item['Slot #'],item['Module']
    if (Slot_No, Module) not in ORDER.keys():
        continue
        #print(Slot_No,Module,type(item['Planned EOP']))
        w1.loc[(Slot_No,Module),:] = pd.Series([np.nan for a in range(w1.shape[1])])
        w1['Module'][(Slot_No,Module)] = Module
        w1['Slot #'][(Slot_No,Module)] = Slot_No
        w1['Planned EOP'][(Slot_No,Module)] = item['Planned EOP']
        print(Slot_No, Module,'Planned_EOP',item['Planned EOP'])
        if pd.isnull(item['Revised Start']):
            if 'NPI' in item['Module']:
                w1['Hol,Wkd,Revised Start'][(Slot_No,Module)]= item['Planned EOP'] - datetime.timedelta(days=80)
            else:
                w1['Hol,Wkd,Revised Start'][(Slot_No,Module)]= item['Planned EOP'] - datetime.timedelta(days=17)
            while  w1['Hol,Wkd,Revised Start'][(Slot_No,Module)] in Holidays_And_Weekends:
                w1['Hol,Wkd,Revised Start'][(Slot_No,Module)] += datetime.timedelta(days=1)
            item['Revised Start'] = w1['Hol,Wkd,Revised Start'][(Slot_No,Module)]
        ORDER[(item['Slot #'],item['Module'])] = OrderAndModule(item['Customer'],item['Slot #'],item['Module'],item['Comp Date Revised EOP'],item['Planned EOP'],item['Revised Start'], item['Planned Build Start'],item['Planned Test Start'],item['Revised Start'])
    print(item['Slot #'],item['Module'],item['Revised Start'])
    if pd.isnull(item['Int Days']) != True:
        ORDER[(item['Slot #'],item['Module'])].Int_Days = item['Int Days']
        #w1['Int'][(Slot_No,Module)] = item['Int Days']
    elif pd.isnull(item['Revised Start']) == False and pd.isnull(item['Planned Test Start']) == False:
        ORDER[(item['Slot #'],item['Module'])].Int_Days = CountDays(item['Revised Start'],item['Planned Test Start'])
    else:
        ORDER[(item['Slot #'],item['Module'])].Int_Days = 8
        #w1['Int'][(Slot_No,Module)] = 8
    if pd.isnull(item['Test Days']) != True:
        ORDER[(item['Slot #'],item['Module'])].Test_Days = item['Test Days']
        #w1['Test'][(Slot_No,Module)] = item['Int Days']
    elif pd.isnull(item['Comp Date Revised EOP']) == False and pd.isnull(item['Planned Test Start']) == False:
        ORDER[(item['Slot #'],item['Module'])].Test_Days = CountDays(item['Planned Test Start'],item['Comp Date Revised EOP']) - 1
    else:
        ORDER[(item['Slot #'],item['Module'])].Test_Days = 7
        #w1['Test'][(Slot_No,Module)] = 7
    if pd.isnull(item['Revised Start']) != True:
        ORDER[(item['Slot #'],item['Module'])].Revised_Start = item['Revised Start']
        new_start_day.append(item['Revised Start'])
        w1['Hol,Wkd,Revised Start'][(Slot_No,Module)] = item['Revised Start']
    if pd.isnull(item['Planned Build Start']) != True:
         w1['Planned Build Start'][(Slot_No,Module)] = item['Planned Build Start']
    if pd.isnull(item['Planned Test Start']) != True:
         w1['Planned Test Start'][(Slot_No,Module)] = item['Planned Test Start']
    if pd.isnull(item['Comp Date Revised EOP']) != True:
         w1['Comp Date Revised EOP'][(Slot_No,Module)] = item['Comp Date Revised EOP']
    if pd.isnull(item['Planned EOP']) != True:
         w1['Planned EOP'][(Slot_No,Module)] = item['Planned EOP']
         
    print(True)
    Slot_No,Module, Revised_Start, Int_Days, Test_Days = item['Slot #'],item['Module'],ORDER[(item['Slot #'],item['Module'])].Revised_Start, ORDER[(item['Slot #'],item['Module'])].Int_Days, ORDER[(item['Slot #'],item['Module'])].Test_Days
    w1, ORDER = Update(w1, ORDER, Slot_No, Module, Revised_Start, Int_Days, Test_Days) 
    for t in Time_List_Index:
        if t in Holidays_And_Weekends:
            w1[t][(Slot_No,Module)] = 'Hol, Wkd'
if pd.isnull(dataf['Reflow Start Day'][1]) == False:
    Reflow_Start_Date = dataf['Reflow Start Day'][1]
else:
    Reflow_Start_Date = min(new_start_day)
# Generate priorities of the orders based on Planned EOP
Priority = sorted(OrderAndModule.Priority, key = lambda i:i[0])
# Make the (order,module) as key, priority as value in a hashtable
ID = {}
for i in range(len(Priority)):
    ID[Priority[i][1:]] = i
# Inverse the key and value in the hashtable, prority is the key and (order, module) is the table
IDInv = {}
for key,value in ID.items():
    IDInv[value] = key
#print(IDInv)
#Initiate Bay Capacities
CP = {}
for i in Time_List_Index:
    if i < datetime.datetime(2022,1,1,0,0):
        CP[('Int',i)] = 19
        CP[('PolTest',i)] = 4
        CP[('Test',i)] = 14
        CP[('Start',i)] = 2
        CP[('NPIInt',i)] = 3
    else: 
        CP[('Int',i)] = 19
        CP[('PolTest',i)] = 4
        CP[('Test',i)] = 15
        CP[('Start',i)] = 2
        CP[('NPIInt',i)] = 3
# Check initial capacities

'''
 code example: rebuild an integration bay into test bay in 2/1/2022
 for i in Time_List_Index:
    if i < datetime.datetime(2022,1,1,0,0):
        CP[('Int',i)] = 19
        CP[('PolTest',i)] = 4
        CP[('Test',i)] = 14
        CP[('Start',i)] = 2
        CP[('NPIInt',i)] = 3
    elif i < datetime.datetime(2022,2,1,0,0):: 
        CP[('Int',i)] = 19
        CP[('PolTest',i)] = 4
        CP[('Test',i)] = 15
        CP[('Start',i)] = 2
        CP[('NPIInt',i)] = 3
    else:
        CP[('Int',i)] = 18
        CP[('PolTest',i)] = 4
        CP[('Test',i)] = 16
        CP[('Start',i)] = 2
        CP[('NPIInt',i)] = 3
'''       

Int_Total,Int_Clnr,Int_Pol,Test_Total,Test_Clnr,Test_Pol,Kit_Total,Start,NPI_Total = CalBaysCapacity(w1)
#print('Reading File Time',time.time()-starttime)


# In[280]:

print('Reflow_Start_Date:',Reflow_Start_Date)
w1,ORDER = Reflow(w1,Reflow_Start_Date, Time_List_Index[-3],ORDER)
#print('Reflow Time',time.time()-starttime)


# In[281]:


MPP = pd.read_csv('MPP File.csv')
MPP = MPP[MPP['Build BU Name'] == 'D9']
MPP = MPP[MPP['EOP Fiscal Quarter'] >= '2021Q4']
MPP = MPP[MPP['Plant'] == 4070]
MPP = MPP.drop_duplicates(subset=['Machine #'])
MPP['Machine #'] = MPP['Machine #']
MPP['SOP Actual'] = pd.to_datetime(MPP['SOP Actual'],errors='ignore')
MPP = MPP.set_index('Machine #')


# In[282]:


for index, item in w1.iterrows():
    if index[0] in MPP.index:
        if '/' in MPP['Ship Revised'][index[0]]:
            w1['Ship Revised'][index] = MPP['Ship Revised'][index[0]]
            shiptime = w1['Ship Revised'][index]
            w1['EOP DDD'][index] = datetime.datetime.strptime(shiptime, '%m/%d/%y') - datetime.timedelta(days=5)
            w1['EOP to Cust Commit Days'][index] = (w1['EOP DDD'][index] - w1['Comp Date Revised EOP'][index]).days
            w1['EOP DDD'][index] = str(w1['EOP DDD'][index])[:10]
    if str(item['Revised Start'])[0] == '2':
        w1['Hol,Wkd,Revised Start'][index] = str(item['Revised Start'])[:10]
    if str(item['Planned Build Start'])[0] == '2':
        w1['Planned Build Start'][index] = str(item['Planned Build Start'])[:10]
    if str(item['Planned Test Start'])[0] == '2':
        w1['Planned Test Start'][index] = str(item['Planned Test Start'])[:10]
    if str(item['Comp Date Revised EOP'])[0] == '2':
        w1['Comp Date Revised EOP'][index] = str(item['Comp Date Revised EOP'])[:10]
    if str(item['Planned EOP'])[0] == '2':
        w1['Planned EOP'][index] = str(item['Planned EOP'])[:10]
    w1['Build Cycle Time'][index] = item['Int'] + item['Final Test']


# ## Save

# In[283]:


blank = [np.nan for i in range(17)]
Int_Total,Int_Clnr,Int_Pol,Test_Total,Test_Clnr,Test_Pol,Kit_Total,Start,NPI_Total = CalBaysCapacity(w1)
r1 = blank + ['# NPI in INT'] + [len(NPI_Total[t]) for t in Time_List_Index]
r2 = blank + ['# Total in INT'] + [len(Int_Total[t]) for t in Time_List_Index]
r3 = blank + ['# Pol in TEST'] + [len(Test_Pol[t]) for t in Time_List_Index]
r4 = blank + ['# Total in Test'] + [len(Test_Total[t]) for t in Time_List_Index]
r6 = blank + ['# Total in Kit'] + [len(Kit_Total[t]) for t in Time_List_Index]
r5 = w1.columns.tolist()
df = pd.DataFrame([r1,r2,r3,r4,r6,r5],index = [-1,-2,-3,-4,-5,-6],columns = r5)
w2 = w1.copy()
w3 = w2.reset_index(drop=True)
w3 = w3.sort_values(by=['Hol,Wkd,Revised Start'],ascending=True)
w4 = pd.concat([df,w3])
for index, item in w4.iterrows():
    for c in r5:
        if type(w4[c][index]) == datetime.datetime:
            w4[c][index] = str(w4[c][index])[:11]


# In[284]:


w = w4.style.applymap(highlight_cells)#\.set_table_style()


# In[285]:


# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter(File_Name+'.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
w.to_excel(writer, sheet_name='Sheet1')
# Close the Pandas Excel writer and output the Excel file.
writer.save()
print('Running Time',time.time()-starttime,'s')

