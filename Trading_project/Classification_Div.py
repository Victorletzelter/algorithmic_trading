#This code has been written by Victor LETZELTER and Hugo BESSON.

#This file allows to detect the four divergences types, given : 
#- An asset (here, AAPL has been chosen) associated with a resolution, and a time interval.
#- An oscillator : here, the RSI. 

import os
print("Current Working Directory " , os.getcwd())
os.chdir("/Users/victorletzelter/Documents/GitHub/algorithmic_trading/Trading_project")

#The next two scripts are to execute before launching the code 

exec(open('Imports.py').read())
exec(open('Functions_algo.py').read())

import yfinance as yf  

data = yf.Ticker("AAPL") #AAPL can be replaced by the desired asset
dataDF = data.history(interval='1h',start='2021-2-1',end=dt.datetime.now()) 

l=dataDF['Close']
l=l.tolist()
(Mins,indMin,Maxs,indMax)=Extremas(l)

plt.plot(l,color='black')
plt.xlabel('Point Number')
plt.ylabel('Asset values ($)')
plt.title('Evolution of the asset chosen in a given time interval')
plt.grid()
plt.show()

dataDF=Creation_rsi(dataDF)
l2=dataDF['RSI']
l2=l2.tolist()
(Mins2,indMin2,Maxs2,indMax2)=Extremas(l2)

plt.plot(l2)
plt.xlabel('Point Number')
plt.ylabel('RSI value')
plt.title('Evolution of the RSI in the same time interval')
plt.grid()
plt.show()

#Hausses_interessantes_cours=pt_interessant(indMax,"cours",l,l2)
#Baisses_interessantes_rsi=pt_interessant(indMax2,'RSI',l,l2)
#Divergence=creation_divergence(Hausses_interessantes_cours,Baisses_interessantes_rsi)
#Divergence_filtree=Filtration(Divergence)

###Classification

#Bearish 
#plusHautBas="Haut" (car Bearish)
PHHausses_interessantes_cours=pt_interessant_typeDiv(indMax,"cours",l,l2,"Haut","RegularBearish",long=50)
PHBaisses_interessantes_rsi=pt_interessant_typeDiv(indMax2,"RSI",l,l2,"Haut","RegularBearish",long=50)
PHBaisses_interessantes_cours=pt_interessant_typeDiv(indMax,"cours",l,l2,"Haut","HiddenBearish",long=50)
PHHausses_interessantes_rsi=pt_interessant_typeDiv(indMax2,"RSI",l,l2,"Haut","HiddenBearish",long=50)

#BRTrace2(PHHausses_interessantes_rsi,PHBaisses_interessantes_rsi,Mins,indMin,Maxs,indMax,l2)

#Bearish Regular
BearRegDivergence=creation_divergenceBearReg(PHHausses_interessantes_cours,PHBaisses_interessantes_rsi)
BearRegDivergence_filtree=Filtration(BearRegDivergence)
BRTraceFinaux(BearRegDivergence_filtree)

effects=[]
for e in BearRegDivergence_filtree :
    if Effect(e,l,'bear')!=None :
        effects.append(Effect(e,l,'bear'))

plt.hist((effects))
plt.show()
    

#Bearish Hidden
BearHiddenDivergence=creation_divergenceBearHidden(PHBaisses_interessantes_cours,PHHausses_interessantes_rsi)
BearHiddenDivergence_filtree=Filtration(BearHiddenDivergence)
BRTraceFinaux(BearHiddenDivergence_filtree)

for e in BearHiddenDivergence_filtree :
    print(Effect(e,l,'bear'))

#Bullish
#plusHautBas="Bas" (car Bullish)
#Bearish 
#plusHautBas="Haut" (car Bearish)

PBBaisses_interessantes_cours=pt_interessant_typeDiv(indMin,"cours",l,l2,"Bas","RegularBullish",long=50)
PBHausses_interessantes_rsi=pt_interessant_typeDiv(indMin2,"RSI",l,l2,"Bas","RegularBullish",long=50)
PBHausses_interessantes_cours=pt_interessant_typeDiv(indMin,"cours",l,l2,"Bas","HiddenBullish",long=50)
PBBaisses_interessantes_rsi=pt_interessant_typeDiv(indMin2,"RSI",l,l2,"Bas","HiddenBullish",long=50)

#BRTrace2(PBHausses_interessantes_cours,PBBaisses_interessantes_cours,Mins,indMin,Maxs,indMax,l)
#BRTrace2(PBHausses_interessantes_rsi,PBBaisses_interessantes_rsi,Mins,indMin,Maxs,indMax,l2)

#Bullish Regular
BullRegDivergence=creation_divergenceBullReg(PBBaisses_interessantes_cours,PBHausses_interessantes_rsi)
BullRegDivergence_filtree=Filtration(BullRegDivergence)
BRTraceFinaux(BullRegDivergence_filtree,title='Bull',color='blue')

le=[]
for e in BullRegDivergence_filtree :
    le.append(Effect(e,l,'bull'))

#Bullish Hidden
BullHiddenDivergence=creation_divergenceBullHidden(PBHausses_interessantes_cours,PBBaisses_interessantes_rsi)
BullHiddenDivergence_filtree=Filtration(BullHiddenDivergence)
BRTraceFinaux(BullHiddenDivergence)

le=[]
for e in BullHiddenDivergence_filtree :
    if Effect(e,l,'bull')!=None :
        le.append(Effect(e,l,'bull'))

print(GlobalPerf(BearRegDivergence_filtree,l,'bear'))






