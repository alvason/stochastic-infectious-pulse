
# coding: utf-8

# # Stochastic infectious pulse
# https://github.com/alvason/stochastic-infectious-pulse
# 
# ### Stochastic version for evolutionary insights

# In[1]:

'''
author: Alvason Zhenhua Li
date:   07/07/2015
'''
get_ipython().magic(u'matplotlib inline')

import numpy as np
import matplotlib.pyplot as plt
import time
import os
dir_path = '/Users/al/Desktop/GitHub/stochastic-infectious-pulse/figure'
file_name = 'stochastic-sir'

import alva_machinery_probability as alva

AlvaFontSize = 23
AlvaFigSize = (16, 8)
numberingFig = 0

# stochastic evolution
figure_name = '-stochastic-event'
file_suffix = '.png'
save_figure = os.path.join(dir_path, file_name + figure_name + file_suffix)
text_list = [r'$ Stochastic-SIR-evolution(all \ possible \ evolving \ events): $'
              , r'$ 1. event(new \ SIR \ in)  = \mu(S+I+R) $'
              , r'$ 2. event(old \ S \ out) = \mu S $'
              , r'$ 3. event(old \ I \ out) = \mu I $'
              , r'$ 4. event(old \ R \ out) = \mu R $'
              , r'$ 5. event(SI \ infected) = \beta S(t)I(t) $' 
              , r'$ 6. event(IR \ recovred) = \gamma I(t) $']
total_list = np.size(text_list)
numberingFig = numberingFig + 1
plt.figure(numberingFig, figsize=(total_list*2, total_list))
plt.axis('off')
for i in range(total_list):
    plt.text(0, (total_list - float(i))/total_list
             , text_list[i].replace('\\\n', '')
             , fontsize = 1.2*AlvaFontSize)
plt.savefig(save_figure, dpi = 100)
plt.show()

# relating to the deterministic SIR equation
text_list = [r'$ Corresponding \ to \ deterministic-SIR-equation $'
             , r'$ \frac{\partial S(t)}{\partial t} = \
                   -\beta S(t)I(t) +\mu N -\mu S(t) $'
             , r'$ \frac{\partial I(t)}{\partial t} = \
                   +\beta S(t)I(t) - \gamma I(t) -\mu I(t) $'
             , r'$ \frac{\partial R(t)}{\partial t} = \
                   +\gamma I(t) - \mu R(t) $']
total_list = np.size(text_list)
numberingFig = numberingFig + 1
plt.figure(numberingFig, figsize=(total_list*2, total_list))
plt.axis('off')
for i in range(total_list):
    plt.text(0, (total_list - float(i))/total_list
             , text_list[i].replace('\\\n', '')
             , fontsize = 1.2*AlvaFontSize)
plt.show()


# In[2]:

# algorithm for stochastic evolution
figure_name = '-Gillespie-algorithm'
file_suffix = '.png'
save_figure = os.path.join(dir_path, file_name + figure_name + file_suffix)
text_list = [r'$ Gillespie-algorithm: $'
             , r'$ 1. \ initialize \ the \ number \ of \ each \ group: \ S(t=0), I(t=0), R(t=0) $'
             , r'$ 2. \ compute \ the \ probability \ of \ each \ possible \ event_i \ at \ the \ moment \ \bf{t} $'
             , r'$ 3. \ randomly \ select \ event_{next} \
                   \ according \ to \ random{[0,1)} < \frac{\sum_{k=1}^{next}event_{k}}{\sum_{i=1}^{all} event_i} $'
             , r'$ 4. \ update \ the \ number \ of \ corresponding \ group $'
             , r'$ 5. \ compute \ \Delta t = \frac{-log_{e}(event_{next})}{\sum_{i}^{} event_i} $'
             , r'$ \ (according \ to \ probability-density-function: \ Pr(t < event_{next} < t+\Delta t) = \
                   exp(-\Delta t \sum_{i}^{} event_i )) $'
             , r'$ 7. \ update \ t = t + \Delta t $'
             , r'$ 6. \ go \ to \ step-2 $'
            ]
total_list = np.size(text_list)
numberingFig = numberingFig + 1
plt.figure(numberingFig, figsize=(total_list, total_list*1.5))
plt.axis('off')
for i in range(total_list):
    plt.text(0, (total_list - float(i))/total_list
             , text_list[i].replace('\\\n', '')
             , fontsize = 1.2*AlvaFontSize)
plt.savefig(save_figure, dpi = 100)
plt.show()


# In[3]:

''' define stochasticSIR function '''
def stochasticSIR(minT, maxT, totalStep_T, initial_S, initial_I, initial_R
                  , reprodNum, recovRate, inOutRate, infecRate):
    # intialized
    gT = np.zeros([totalStep_T]) 
    gS = np.zeros([totalStep_T]) 
    gI = np.zeros([totalStep_T]) 
    gR = np.zeros([totalStep_T]) 
    tn = int(0)
    gT[tn] = minT
    gS[tn] = initial_S
    gI[tn] = initial_I
    gR[tn] = initial_R  
    # all possible events
    event_SIRin = inOutRate*(gS[tn] + gI[tn] + gR[tn])
    event_Sout = inOutRate*gS[tn]
    event_Iout = inOutRate*gI[tn]
    event_Rout = inOutRate*gR[tn]
    event_SI = infecRate*gS[tn]*gI[tn] / (gS[tn] + gI[tn] + gR[tn])
    event_IR = recovRate*gI[tn]
    # configuration table
    eventRate_updateNumSIR = np.array([[event_SIRin, +1, 0, 0]
                                     , [event_Sout, -1, 0, 0]
                                     , [event_Iout, 0, -1, 0]
                                     , [event_Rout, 0, 0, -1]
                                     , [event_SI, -1, +1, 0]
                                     , [event_IR, 0, -1, +1]])
    ###
    while (gT[tn] < maxT):       
        # randomly choose event
        if np.random.random() < (eventRate_updateNumSIR[0:1, 0].sum() / eventRate_updateNumSIR[:, 0].sum()):
            en = 0
        elif np.random.random() < (eventRate_updateNumSIR[0:2, 0].sum() / eventRate_updateNumSIR[:, 0].sum()):
            en = 1
        elif np.random.random() < (eventRate_updateNumSIR[0:3, 0].sum() / eventRate_updateNumSIR[:, 0].sum()):
            en = 2
        elif np.random.random() < (eventRate_updateNumSIR[0:4, 0].sum() / eventRate_updateNumSIR[:, 0].sum()):
            en = 3
        elif np.random.random() < (eventRate_updateNumSIR[0:5, 0].sum() / eventRate_updateNumSIR[:, 0].sum()):
            en = 4
        else:
            en = 5
        # update number of section
        gS[tn] = gS[tn] + eventRate_updateNumSIR[en, 1]
        gI[tn] = gI[tn] + eventRate_updateNumSIR[en, 2]
        gR[tn] = gR[tn] + eventRate_updateNumSIR[en, 3]
        # update event_rate
        event_SIRin = inOutRate*(gS[tn] + gI[tn] + gR[tn])
        event_Sout = inOutRate*gS[tn]
        event_Iout = inOutRate*gI[tn]
        event_Rout = inOutRate*gR[tn]
        event_SI = infecRate*gS[tn]*gI[tn] / (gS[tn] + gI[tn] + gR[tn])
        event_IR = recovRate*gI[tn]
        eventRate_updateNumSIR = np.array([[event_SIRin, 1, 0, 0]
                                         , [event_Sout, -1, 0, 0]
                                         , [event_Iout, 0, -1, 0]
                                         , [event_Rout, 0, 0, -1]
                                         , [event_SI, -1, +1, 0]
                                         , [event_IR, 0, -1, +1]])  
        # next step is based on current step
        dt = -np.log(np.random.random()) / eventRate_updateNumSIR[:, 0].sum()
        gT[tn + 1] = gT[tn] + dt 
        gS[tn + 1] = gS[tn]
        gI[tn + 1] = gI[tn]
        gR[tn + 1] = gR[tn]
        tn = tn + 1
    # set the value of remaining steps = value of the last step (for ending)
    gT[tn:] = gT[tn]
    gS[tn:] = gS[tn]
    gI[tn:] = gI[tn]
    gR[tn:] = gR[tn]
    ###
    return(gT, gS, gI, gR)


# In[4]:

''' starting from one infected '''
# setting parameter
timeUnit = 'day'
if timeUnit == 'day':
    day = 1
    year = 365 
elif timeUnit == 'year':
    year = 1
    day = float(1)/365 
    
total_SIR = 300
initial_I = 1
initial_S = total_SIR - initial_I
initial_R = total_SIR - initial_S - initial_I
# set parameter
reprodNum = float(1.5) # basic reproductive number R0: one infected person will transmit to 1.8 person 
recovRate = float(1)/(4*day) # 4 days per period ==> rate/year = 365/4
inOutRate = float(1)/(30*year) # birth rate per year
infecRate = reprodNum*(recovRate + inOutRate)/1 # per year, per person, per total-population

# initial boundary condition
minT = float(0*day)
maxT = float(90*day)

totalStep_T = int(maxT*total_SIR)
# stochastic evolution way
total_way = int(5)
gTT = np.zeros([total_way, totalStep_T]) 
gSS = np.zeros([total_way, totalStep_T]) 
gII = np.zeros([total_way, totalStep_T]) 
gRR = np.zeros([total_way, totalStep_T]) 

for wn in range(total_way):
    evolution = stochasticSIR(minT, maxT, totalStep_T, initial_S, initial_I, initial_R
                        , reprodNum, recovRate, inOutRate, infecRate)
    gTT[wn] = evolution[0]
    gSS[wn] = evolution[1]
    gII[wn] = evolution[2]
    gRR[wn] = evolution[3]

# plotting
figure_name = '-sir'
file_suffix = '.png'
save_figure = os.path.join(dir_path, file_name + figure_name + file_suffix)

numberingFig = numberingFig + 1
figure = plt.figure(numberingFig, figsize = AlvaFigSize)
for wn in range(total_way):
    plt.plot(gTT[wn], gSS[wn], label = r'$ S_{:}(t) $'.format(wn), linewidth = (1 + wn)
             , color = 'blue', alpha = float(0.5 + wn/total_way))
    plt.plot(gTT[wn], gII[wn], label = r'$ I_{:}(t) $'.format(wn), linewidth = (1 + wn)
             , color = 'red', alpha = float(0.5 + wn/total_way))
    plt.plot(gTT[wn], gRR[wn], label = r'$ R_{:}(t) $'.format(wn), linewidth = (1 + wn)
             , color = 'green', alpha = float(0.5 + wn/total_way))
    plt.plot(gTT[wn], (gSS[wn] + gII[wn] + gRR[wn]), label = r'$ N_{:}(t) $'.format(wn)
             , linewidth = (1 + wn), color = 'black', alpha = float(0.5 + wn/total_way))    
plt.grid(True)
plt.title(r'$ Stochastic \ SIR \ (Susceptible-Infected-Recovered) $', fontsize = AlvaFontSize)
plt.xlabel(r'$ time \ ({:})$'.format(timeUnit), fontsize = AlvaFontSize)
plt.ylabel(r'$ Population $', fontsize = AlvaFontSize)
plt.legend(loc = (1, 0))
plt.text(maxT, total_SIR*6.0/6, r'$ R_0 = {:} $'.format(reprodNum), fontsize = AlvaFontSize)
plt.text(maxT, total_SIR*5.0/6, r'$ \gamma = {:} $'.format(recovRate), fontsize = AlvaFontSize)
plt.text(maxT, total_SIR*4.0/6, r'$ \beta = {:} $'.format(infecRate), fontsize = AlvaFontSize)
plt.text(maxT, total_SIR*3.0/6, r'$ \mu = {:} $'.format(inOutRate), fontsize = AlvaFontSize)
plt.xticks(fontsize = AlvaFontSize*0.7)
plt.yticks(fontsize = AlvaFontSize*0.7) 
figure.tight_layout()
plt.savefig(save_figure, dpi = 100, bbox_inches='tight')
plt.show()


# In[ ]:



