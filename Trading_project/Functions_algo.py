def Extremas(l) :

    lclean=[]
    for e in l :
        if not(math.isnan(e)) :
            lclean.append(e)
    
    #Détection des minimums locaux

    indMin, _=find_peaks(max(np.abs(lclean))-l,height=0)    #indMin : indices des minimums locaux
    Mins=[l[e] for e in indMin]
    #indMin=l.index[indMin]

    #Détection des maximums locaux

    indMax, _ = find_peaks(l,height=0)    #indMax : indices des maximums locaux
    Maxs=[l[e] for e in indMax]
    #indMax=l.index[indMax]

    return(Mins,indMin,Maxs,indMax)

def Creation_rsi(dataDF) :
    ###RSI

    dataDF['Up Move'] = np.nan
    dataDF['Down Move'] = np.nan
    dataDF['Average Up'] = np.nan
    dataDF['Average Down'] = np.nan
    # Relative Strength
    dataDF['RS'] = np.nan
    # Relative Strength Index
    dataDF['RSI'] = np.nan
    ## Calculate Up Move & Down Move
    for x in range(1, len(dataDF)):
        dataDF['Up Move'][x] = 0
        dataDF['Down Move'][x] = 0

        if dataDF['Close'][x] > dataDF['Close'][x-1]:
            dataDF['Up Move'][x] = dataDF['Close'][x] - dataDF['Close'][x-1]

        if dataDF['Close'][x] < dataDF['Close'][x-1]:
            dataDF['Down Move'][x] = abs(dataDF['Close'][x] - dataDF['Close'][x-1])

    ## Calculate initial Average Up & Down, RS and RSI
    dataDF['Average Up'][14] = dataDF['Up Move'][1:15].mean()
    dataDF['Average Down'][14] = dataDF['Down Move'][1:15].mean()
    dataDF['RS'][14] = dataDF['Average Up'][14] / dataDF['Average Down'][14]
    dataDF['RSI'][14] = 100 - (100/(1+dataDF['RS'][14]))
    ## Calculate rest of Average Up, Average Down, RS, RSI
    for x in range(15, len(dataDF)):
        dataDF['Average Up'][x] = (dataDF['Average Up'][x-1]*13+dataDF['Up Move'][x])/14
        dataDF['Average Down'][x] = (dataDF['Average Down'][x-1]*13+dataDF['Down Move'][x])/14
        dataDF['RS'][x] = dataDF['Average Up'][x] / dataDF['Average Down'][x]
        dataDF['RSI'][x] = 100 - (100/(1+dataDF['RS'][x]))

    dataDF2=pd.DataFrame.copy(dataDF)
    stock = sdf.retype(dataDF2)

    def BRTrace3() :
        fig, axs = plt.subplots(2)
        fig.suptitle('Vertically stacked subplots')
        axs[0].plot(stock['rsi'],'y')
        axs[1].plot(dataDF['Close'],'r')
        plt.show()

    return(stock)

def tracerDroite(ind,val,tend):
    x=np.linspace(ind[0],ind[1],(ind[1]-ind[0])*10)
    A=(val[1]-val[0])/(ind[1]-ind[0])
    B=val[0]-A*ind[0]
    y=A*x + B
    if tend=="hausse":
        plt.plot(x,y,'r')
    else :
        plt.plot(x,y,'b')

def Creation_rsi(dataDF) :

    dataDF['Up Move'] = np.nan
    dataDF['Down Move'] = np.nan
    dataDF['Average Up'] = np.nan
    dataDF['Average Down'] = np.nan
    # Relative Strength
    dataDF['RS'] = np.nan
    # Relative Strength Index
    dataDF['RSI'] = np.nan
    for x in range(1, len(dataDF)):
        dataDF['Up Move'][x] = 0
        dataDF['Down Move'][x] = 0

        if dataDF['Close'][x] > dataDF['Close'][x-1]:
            dataDF['Up Move'][x] = dataDF['Close'][x] - dataDF['Close'][x-1]

        if dataDF['Close'][x] < dataDF['Close'][x-1]:
            dataDF['Down Move'][x] = abs(dataDF['Close'][x] - dataDF['Close'][x-1])

    dataDF['Average Up'][14] = dataDF['Up Move'][1:15].mean()
    dataDF['Average Down'][14] = dataDF['Down Move'][1:15].mean()
    dataDF['RS'][14] = dataDF['Average Up'][14] / dataDF['Average Down'][14]
    dataDF['RSI'][14] = 100 - (100/(1+dataDF['RS'][14]))

    for x in range(15, len(dataDF)):
        dataDF['Average Up'][x] = (dataDF['Average Up'][x-1]*13+dataDF['Up Move'][x])/14
        dataDF['Average Down'][x] = (dataDF['Average Down'][x-1]*13+dataDF['Down Move'][x])/14
        dataDF['RS'][x] = dataDF['Average Up'][x] / dataDF['Average Down'][x]
        dataDF['RSI'][x] = 100 - (100/(1+dataDF['RS'][x]))

    return(dataDF)

def coupe(indice_debut,indice_fin,cours,plus_HautBas) :

    x=np.arange(indice_debut+1,indice_fin) #1 point en abscisse par UT.
    indices=[indice_debut,indice_fin]
    valeurs=[dataDF[cours][indice_debut],dataDF[cours][indice_fin]]

    if plus_HautBas=="Haut" : #(On regarde les plus hauts du cours) : on vérifie si ça monte
        for e in x :
            if dataDF[cours][e]>droite(e,indices,valeurs) :
                return(True)

    if plus_HautBas=="Bas" : #(On regarde les plus bas du cours) : on vérifie si ça baisse
        for e in x :
            if dataDF[cours][e]<droite(e,indices,valeurs) :
                return(True)
    return(False)

def droite(x,indices,valeurs) :
    coeff=(valeurs[1]-valeurs[0])/(indices[1]-indices[0])
    b=valeurs[0]-coeff*indices[0]
    return(coeff*x+b)

def test_coupe(i,j) :
    print(coupe(i,j,'Close',"Haut"))

def tracerDroite(ind,val,tend):
    x=np.linspace(ind[0],ind[1],(ind[1]-ind[0])*10)
    A=(val[1]-val[0])/(ind[1]-ind[0])
    B=val[0]-A*ind[0]
    y=A*x + B
    if tend=="hausse":
        plt.plot(x,y,'r')
    else :
        plt.plot(x,y,'b')

def Mouvements(indMin,indMax,l) :
    #Detection des tendances

    Hausses=[] #liste contenant les tuples haussiers
    Baisses=[] #liste contenant les tuples baissiers

    '''Détection des hausses'''
    i=0
    lenMax=len(indMax)
    while i<lenMax:
        j=i
        while j<(lenMax-1) and l[indMax[j+1]]>l[indMax[j]] :
            j+=1
        if i<j:
            Hausses.append((indMax[i],indMax[j]))
        i=j+1

    '''Détection des baisses'''
    i=0
    lenMin=len(indMin)
    while i<lenMin:
        j=i
        while j<(lenMin-1) and l[indMin[j+1]]<l[indMin[j]] :
            j+=1
        if i<j:
            Baisses.append((indMin[i],indMin[j]))

        i=j+1

    return(Hausses,Baisses)

def point_de_depart(delai,adx_moy) :

    valeur=len(dataDF)-delai

    while adx_moy[valeur]>=25 :
        valeur=valeur-1

    return(valeur)

def BR_pt_interessant(indMax,ID) : #ID = 'RSI' ou ID="cours"

    i=0

    taille=dataDF.shape[0]
    l=np.zeros(taille)
    l2=np.zeros(taille)

    for i in range (taille):
        l[i]=dataDF['Close'][i]

    for i in range (taille):
        l2[i]=dataDF['RSI'][i]
    "H"

    #Détection des minimums locaux

    indMin, _=find_peaks(-l+max(abs(l)),height=0)    #indMin : indices des minimums locaux
    Mins=l[indMin]

    #Détection des maximums locaux

    indMax, _ = find_peaks(l,height=0)    #indMax : indices des maximums locaux
    Maxs=l[indMax]

    liste=[]

    if ID=="cours" :

        while i<len(indMax) :

            Meilleur=0

            for j in range(i,len(indMax)) :
                if l[indMax[j]]>l[indMax[i]] and not(coupe(indMax[i],indMax[j],'Close',"Haut")) :
                    indice=j
                    Meilleur=indMax[j]

            if not(Meilleur==0) :
                liste.append((indMax[i],Meilleur))
                i=indice

            else :
                i=i+1

    if ID=='RSI' :

        while i<len(indMax):

            Meilleur=0

            for j in range(i,len(indMax)) :
                if l2[indMax[j]]<l2[indMax[i]] and not(coupe(indMax[i],indMax[j],'RSI',"Haut")) :
                    indice=j
                    Meilleur=indMax[j]

            if not(Meilleur==0) :
                liste.append((indMax[i],Meilleur))
                i=indice

            else :
                i=i+1

    return(liste)

#def pt_interessant_ss(indMax,ID,l,l2) : #ID = 'RSI' ou ID="cours"

    i=0
    liste=[]
    MatriceEcart=np.zeros((len(indMax),len(indMax)))

    if ID=="cours" :

        while i<len(indMax) :

            Meilleur=0

            for j in range(i,len(indMax)) :
                if l[indMax[j]]>l[indMax[i]] and not(coupe(indMax[i],indMax[j],'Close',"Hausse")) :
                    MatriceEcart[i,j]=l[indMax[j]]-l[indMax[i]]
                    if MatriceEcart[i,j]==np.max(MatriceEcart[i,:]) :
                        indice=j
                        Meilleur=indMax[j]

            if not(Meilleur==0) :
                liste.append((indMax[i],Meilleur))
                i=indice

            else :
                i=i+1

    if ID=='RSI' :

        while i<len(indMax):

            Meilleur=0

            for j in range(i,len(indMax)) :
                if l2[indMax[j]]<l2[indMax[i]] and not(coupe(indMax[i],indMax[j],'RSI',"Hausse")) :
                    MatriceEcart[i,j]=l2[indMax[i]]-l2[indMax[j]]
                    if MatriceEcart[i,j]==np.max(MatriceEcart[i,:]) :
                        indice=j
                        Meilleur=indMax[j]

            if not(Meilleur==0) :
                liste.append((indMax[i],Meilleur))
                i=indice

            else :
                i=i+1

    return(liste)

def pt_interessant(indMax,ID,l,l2,long=50) : #ID = 'RSI' ou ID="cours"

    i=0
    liste=[]
    MatriceEcart=np.zeros((len(indMax),len(indMax)))

    if ID=="cours" :

        while i<len(indMax) :

            Meilleur=0

            for j in range(i,min(i+long,len(indMax))) :
                if l[indMax[j]]>l[indMax[i]] and not(coupe(indMax[i],indMax[j],'Close',"Haut")) :
                    MatriceEcart[i,j]=l[indMax[j]]-l[indMax[i]]
                    if MatriceEcart[i,j]==np.max(MatriceEcart[i,:]) :
                        indice=j
                        Meilleur=indMax[j]

            if not(Meilleur==0) :
                liste.append((indMax[i],Meilleur))
                i=indice

            else :
                i=i+1

    if ID=='RSI' :

        while i<len(indMax):

            Meilleur=0

            for j in range(i,min(i+long,len(indMax))) :
                if l2[indMax[j]]<l2[indMax[i]] and not(coupe(indMax[i],indMax[j],'RSI',"Haut")) :
                    MatriceEcart[i,j]=l2[indMax[i]]-l2[indMax[j]]
                    if MatriceEcart[i,j]==np.max(MatriceEcart[i,:]) :
                        indice=j
                        Meilleur=indMax[j]

            if not(Meilleur==0) :
                liste.append((indMax[i],Meilleur))
                i=indice

            else :
                i=i+1

    return(liste)

def pt_interessant_type(indMax,ID,l,l2,plusHautBas,long=50) : #ID = 'RSI' ou ID="cours"

    i=0
    liste=[]
    MatriceEcart=np.zeros((len(indMax),len(indMax)))

    if ID=="cours" :

        while i<len(indMax) :

            Meilleur=0

            for j in range(i,min(i+long,len(indMax))) :
                if l[indMax[j]]>l[indMax[i]] and not(coupe(indMax[i],indMax[j],'Close',plusHautBas)) :
                    MatriceEcart[i,j]=l[indMax[j]]-l[indMax[i]]
                    if MatriceEcart[i,j]==np.max(MatriceEcart[i,:]) :
                        indice=j
                        Meilleur=indMax[j]

            if not(Meilleur==0) :
                liste.append((indMax[i],Meilleur))
                i=indice

            else :
                i=i+1

    if ID=='RSI' :

        while i<len(indMax):

            Meilleur=0

            for j in range(i,min(i+long,len(indMax))) :
                if l2[indMax[j]]<l2[indMax[i]] and not(coupe(indMax[i],indMax[j],'RSI',plusHautBas)) :
                    MatriceEcart[i,j]=l2[indMax[i]]-l2[indMax[j]]
                    if MatriceEcart[i,j]==np.max(MatriceEcart[i,:]) :
                        indice=j
                        Meilleur=indMax[j]

            if not(Meilleur==0) :
                liste.append((indMax[i],Meilleur))
                i=indice

            else :
                i=i+1

    return(liste)

def pt_interessant_typeHidden(indMax,ID,l,l2,plusHautBas,long=50) : #ID = 'RSI' ou ID="cours"

    i=0
    liste=[]
    MatriceEcart=np.zeros((len(indMax),len(indMax)))

    if ID=="cours" :

        while i<len(indMax) :

            Meilleur=0

            for j in range(i,min(i+long,len(indMax))) :
                if l[indMax[j]]<l[indMax[i]] and not(coupe(indMax[i],indMax[j],'Close',plusHautBas)) :
                    MatriceEcart[i,j]=l[indMax[i]]-l[indMax[j]]
                    if MatriceEcart[i,j]==np.max(MatriceEcart[i,:]) :
                        indice=j
                        Meilleur=indMax[j]

            if not(Meilleur==0) :
                liste.append((indMax[i],Meilleur))
                i=indice

            else :
                i=i+1

    if ID=='RSI' :

        while i<len(indMax):

            Meilleur=0

            for j in range(i,min(i+long,len(indMax))) :
                if l2[indMax[j]]>l2[indMax[i]] and not(coupe(indMax[i],indMax[j],'RSI',plusHautBas)) :
                    MatriceEcart[i,j]=l2[indMax[j]]-l2[indMax[i]]
                    if MatriceEcart[i,j]==np.max(MatriceEcart[i,:]) :
                        indice=j
                        Meilleur=indMax[j]

            if not(Meilleur==0) :
                liste.append((indMax[i],Meilleur))
                i=indice

            else :
                i=i+1

    return(liste)

def pt_interessant_typeDiv(indM,ID,l,l2,plusHautBas,type_div,long=50) : #ID = 'RSI' ou ID="cours"
    i=0
    liste=[]
    MatriceEcart=np.zeros((len(indM),len(indM)))

    if type_div=='RegularBearish' :
        if ID=="cours" :

            while i<len(indM) :

                Meilleur=0

                for j in range(i,min(i+long,len(indM))) :
                    if l[indM[j]]>l[indM[i]] and not(coupe(indM[i],indM[j],'Close',plusHautBas)) :
                        MatriceEcart[i,j]=l[indM[j]]-l[indM[i]]
                        if MatriceEcart[i,j]==np.max(MatriceEcart[i,:]) :
                            indice=j
                            Meilleur=indM[j]

                if not(Meilleur==0) :
                    liste.append((indM[i],Meilleur))
                    i=indice

                else :
                    i=i+1

        if ID=='RSI' :

            while i<len(indM):

                Meilleur=0

                for j in range(i,min(i+long,len(indM))) :
                    if l2[indM[j]]<l2[indM[i]] and not(coupe(indM[i],indM[j],'RSI',plusHautBas)) :
                        MatriceEcart[i,j]=l2[indM[i]]-l2[indM[j]]
                        if MatriceEcart[i,j]==np.max(MatriceEcart[i,:]) :
                            indice=j
                            Meilleur=indM[j]

                if not(Meilleur==0) :
                    liste.append((indM[i],Meilleur))
                    i=indice

                else :
                    i=i+1

    elif type_div=='HiddenBearish' :
        if ID=="cours" :

            while i<len(indM) :

                Meilleur=0

                for j in range(i,min(i+long,len(indM))) :
                    if l[indM[j]]<l[indM[i]] and not(coupe(indM[i],indM[j],'Close',plusHautBas)) :
                        MatriceEcart[i,j]=l[indM[i]]-l[indM[j]]
                        if MatriceEcart[i,j]==np.max(MatriceEcart[i,:]) :
                            indice=j
                            Meilleur=indM[j]

                if not(Meilleur==0) :
                    liste.append((indM[i],Meilleur))
                    i=indice

                else :
                    i=i+1

        if ID=='RSI' :

            while i<len(indM):

                Meilleur=0

                for j in range(i,min(i+long,len(indM))) :
                    if l2[indM[j]]>l2[indM[i]] and not(coupe(indM[i],indM[j],'RSI',plusHautBas)) :
                        MatriceEcart[i,j]=l2[indM[j]]-l2[indM[i]]
                        if MatriceEcart[i,j]==np.max(MatriceEcart[i,:]) :
                            indice=j
                            Meilleur=indM[j]

                if not(Meilleur==0) :
                    liste.append((indM[i],Meilleur))
                    i=indice

                else :
                    i=i+1

    elif type_div=='RegularBullish' :

        if ID=="cours" :

            while i<len(indM) :

                Meilleur=0

                for j in range(i,min(i+long,len(indM))) :
                    if l[indM[j]]<l[indM[i]] and not(coupe(indM[i],indM[j],'Close',plusHautBas)) :
                        MatriceEcart[i,j]=l[indM[i]]-l[indM[j]]
                        if MatriceEcart[i,j]==np.max(MatriceEcart[i,:]) :
                            indice=j
                            Meilleur=indM[j]

                if not(Meilleur==0) :
                    liste.append((indM[i],Meilleur))
                    i=indice

                else :
                    i=i+1

        if ID=='RSI' :

            while i<len(indM):

                Meilleur=0

                for j in range(i,min(i+long,len(indM))) :
                    if l2[indM[j]]>l2[indM[i]] and not(coupe(indM[i],indM[j],'RSI',plusHautBas)) :
                        MatriceEcart[i,j]=l2[indM[j]]-l2[indM[i]]
                        if MatriceEcart[i,j]==np.max(MatriceEcart[i,:]) :
                            indice=j
                            Meilleur=indM[j]

                if not(Meilleur==0) :
                    liste.append((indM[i],Meilleur))
                    i=indice

                else :
                    i=i+1

    elif type_div=='HiddenBullish' :
        if ID=="cours" :

            while i<len(indM) :

                Meilleur=0

                for j in range(i,min(i+long,len(indM))) :
                    if l[indM[j]]>l[indM[i]] and not(coupe(indM[i],indM[j],'Close',plusHautBas)) :
                        MatriceEcart[i,j]=l[indM[j]]-l[indM[i]]
                        if MatriceEcart[i,j]==np.max(MatriceEcart[i,:]) :
                            indice=j
                            Meilleur=indM[j]

                if not(Meilleur==0) :
                    liste.append((indM[i],Meilleur))
                    i=indice

                else :
                    i=i+1

        if ID=='RSI' :

            while i<len(indM):

                Meilleur=0

                for j in range(i,min(i+long,len(indM))) :
                    if l2[indM[j]]<l2[indM[i]] and not(coupe(indM[i],indM[j],'RSI',plusHautBas)) :
                        MatriceEcart[i,j]=l2[indM[i]]-l2[indM[j]]
                        if MatriceEcart[i,j]==np.max(MatriceEcart[i,:]) :
                            indice=j
                            Meilleur=indM[j]

                if not(Meilleur==0) :
                    liste.append((indM[i],Meilleur))
                    i=indice

                else :
                    i=i+1

  

    return(liste)

def TraceMouvementInt() :
    Hausses_interessante_cours=pt_interessant(indMax,"cours")

    for ind in Hausses_interessante_cours :
        tracerDroite(ind,(l[ind[0]],l[ind[1]]),"hausse")

    plt.plot(l,'k')
    plt.show()

    indMax2, _ = find_peaks(l2,height=0)

    Baisse_interessante_rsi=pt_interessant(indMax2,'RSI')

    for ind in Baisse_interessante_rsi :
       tracerDroite(ind,(l2[ind[0]],l2[ind[1]]),"baisse")

    plt.plot(l2,'k')
    plt.show()

def BR_trace(indMax,l,l2) :

    Hausses_interessante_cours=pt_interessant(indMax,"cours")

    for ind in Hausses_interessante_cours :
        tracerDroite(ind,(l[ind[0]],l[ind[1]]),"hausse")

    plt.plot(l,'k')
    plt.show()


    indMax2, _ = find_peaks(l2,height=0)

    plt.close()

    Baisse_interessante_rsi=pt_interessant(indMax2,'RSI')

    for ind in Baisse_interessante_rsi :
        tracerDroite(ind,(l2[ind[0]],l2[ind[1]]),"hausse")

    plt.plot(l2,'k')
    plt.show()

    Divergence=[]

    for (x,y) in Hausses_interessante_cours :
        if dataDF['RSI'][y]-dataDF['RSI'][x]<=0 :
            if not(coupe(x,y,'RSI',"Haut")) and not((x,y) in Divergence) :
                Divergence.append((x,y))

    for (x,y) in Baisse_interessante_rsi :
        if dataDF['Close'][y]-dataDF['Close'][x]>=0 :
            if not(coupe(x,y,'Close',"Haut")) and not((x,y) in Divergence) :
                Divergence.append((x,y))

def creation_divergence(Hauts_interessante_cours,Baisse_interessante_rsi) :
    Divergence=[]

    for (x,y) in Hausses_interessante_cours :
        if dataDF['RSI'][y]-dataDF['RSI'][x]<=0 :
            if not(coupe(x,y,'RSI',"Haut")) and not((x,y) in Divergence) :
                Divergence.append((x,y))

    for (x,y) in Baisse_interessante_rsi :
        if dataDF['Close'][y]-dataDF['Close'][x]>=0 :
            if not(coupe(x,y,'Close',"Haut")) and not((x,y) in Divergence) :
                Divergence.append((x,y))

    return(Divergence)

#Plus hauts, attentes d'une baisse
def creation_divergenceBearReg(Hausses_interessante_cours,Baisse_interessante_rsi) : 
    Divergence=[]

    for (x,y) in Hausses_interessante_cours :
        if dataDF['RSI'][y]-dataDF['RSI'][x]<=0 :
            if not(coupe(x,y,'RSI',"Haut")) and not((x,y) in Divergence) :
                Divergence.append((x,y))

    for (x,y) in Baisse_interessante_rsi :
        if dataDF['Close'][y]-dataDF['Close'][x]>=0 :
            if not(coupe(x,y,'Close',"Haut")) and not((x,y) in Divergence) :
                Divergence.append((x,y))
    return(Divergence)

def creation_divergenceBearHidden(Baisse_interessante_cours,Hausse_interessante_rsi) : 
    Divergence=[]

    for (x,y) in Baisse_interessante_cours :
        if dataDF['RSI'][y]-dataDF['RSI'][x]>=0 :
            if not(coupe(x,y,'RSI',"Haut")) and not((x,y) in Divergence) :
                Divergence.append((x,y))

    for (x,y) in Hausse_interessante_rsi :
        if dataDF['Close'][y]-dataDF['Close'][x]<=0 :
            if not(coupe(x,y,'Close',"Haut")) and not((x,y) in Divergence) :
                Divergence.append((x,y))
    return(Divergence)

#Plus bas, attente d'une hausse
def creation_divergenceBullReg(Baisse_interessante_cours,Hausse_interessante_rsi) :
    Divergence=[]

    for (x,y) in Baisse_interessante_cours :
        if dataDF['RSI'][y]-dataDF['RSI'][x]>=0 :
            if not(coupe(x,y,'RSI',"Bas")) and not((x,y) in Divergence) :
                Divergence.append((x,y))

    for (x,y) in Hausse_interessante_rsi :
        if dataDF['Close'][y]-dataDF['Close'][x]<=0 :
            if not(coupe(x,y,'Close',"Bas")) and not((x,y) in Divergence) :
                Divergence.append((x,y))
    return(Divergence)

def creation_divergenceBullHidden(Hausse_interessante_cours,Baisse_interessante_rsi) :
    Divergence=[]

    for (x,y) in Hausse_interessante_cours :
        if dataDF['RSI'][y]-dataDF['RSI'][x]<=0 :
            if not(coupe(x,y,'RSI',"Bas")) and not((x,y) in Divergence) :
                Divergence.append((x,y))

    for (x,y) in Baisse_interessante_rsi :
        if dataDF['Close'][y]-dataDF['Close'][x]>=0 :
            if not(coupe(x,y,'Close',"Bas")) and not((x,y) in Divergence) :
                Divergence.append((x,y))
    return(Divergence)

def Score(Divergence) :
    Score=0
    for (x,y) in Divergence :
        Ecart_rsi=(dataDF['RSI'][y]-dataDF['RSI'][x])/dataDF['RSI'][x]
        Ecart_cours=(dataDF['Close'][y]-dataDF['Close'][x])/dataDF['Close'][x]
        Score+=np.abs(Ecart_rsi*Ecart_cours)*(y-x)
    return(Score/len(l))

def Trier(Divergence) :
    liste_len=[y-x for (x,y) in Divergence]
    args=np.argsort(liste_len)
    Divergence_triee=[Divergence[e] for e in args]
    return(Divergence_triee)

def Filtration(Divergence) : #Permet d'éviter le "recouvrement" des divergences
    Divergence_filtree=[]
    Divergence_triee=Trier(Divergence)

    #Indices min et max ?
    min=Divergence[0][0]
    max=Divergence[0][0]
    for i in range (len(Divergence)) :
        for j in range (0,2) :
            if Divergence[i][j]<min :
                min=Divergence[i][j]

            if Divergence[i][j]>max :
                max=Divergence[i][j]

    Liste_presence=np.zeros(max-min)

    for (x,y) in Divergence_triee :
        Clean=0
        for k in range (x-min,y-min) :
            if Liste_presence[k]==0 :
                Liste_presence[k]=1
            else :
                Clean=1
        if Clean==0 and not((x,y) in Divergence_filtree) :
            Divergence_filtree.append((x,y))

    return(Divergence_filtree)

def Filtration_Out(pt_interessant,l,l2) : #Permet de filtrer les points qui ne sont pas dans les zones d'overbought ou d'oversold du RSI
    pt_interessant_f=[]
    for (x,y) in pt_interessant :
        if (l2[x]<=30 and l2[y]<=30) or (l2[x]>=70 and l2[y]>=70) :
            pt_interessant_f.append((x,y))
    return(pt_interessant_f)

def Volatilite(Cours,N) : #N : fenetre
    dataDF_d=dataDF.shift(1)
    logs=np.log(dataDF[Cours].tail(len(dataDF)-1)/dataDF_d[Cours].tail(len(dataDF)-1))
    Vol=np.sqrt(logs.rolling(window=N).var())
    return(Vol)
    #adx_moy = stock['adx'].rolling(window=10).mean()
    #Vol=Volatilite('Close',20)
    #plt.plot(Vol)
    #plt.show()

def BR_trace2(Divergence,dataDF) :
    #### Tracés :

    Divergence_filtree=Filtration(Divergence)

    #Divergence du cours :

    for ind in Divergence_filtree :
        tracerDroite(ind,(dataDF['Close'][ind[0]],dataDF['Close'][ind[1]]),"hausse")


    plt.plot(dataDF['Close'],'k')

    #Divergence du rsi :

    Divergence_filtree=Filtration(Divergence)

    for ind in Divergence_filtree :
        tracerDroite(ind,(dataDF['RSI'][ind[0]],dataDF['RSI'][ind[1]]),"hausse")

    plt.plot(l2,'k')

def BRTraceFinaux(Divergence_filtree,title='Divergence of the asset price',color='red') :
    #### Tracés :

    #Divergence_filtree=Filtration(Divergence)

    #Divergence du cours :
    for ind in Divergence_filtree :
        val=(l[ind[0]],l[ind[1]])
        tracerDroite(ind,(l[ind[0]],l[ind[1]]),"hausse")

    plt.title(title)
    plt.xlabel('Point number')
    plt.grid()
    plt.ylabel('Asset value ($)')
    plt.plot(l,'k')

    for e in Divergence_filtree :
        plt.axvline(e[1],color=color,alpha=0.5)
    plt.show()

    #Divergence du rsi :

    #for ind in Divergence_filtree :
    #    tracerDroite(ind,(l2[ind[0]],l2[ind[1]]),"hausse")

    #plt.title('Divergences in the RSI')
    #plt.plot(l2,'k')
    #plt.show()

def BRTraceFinaux2(Divergence_filtree) :
    #### Tracés :

    fig, ax = plt.subplots(2, figsize=(8, 7))

    #Divergence_filtree=Filtration(Divergence)
    for ind in Divergence_filtree :
        val=(l[ind[0]],l[ind[1]])
        x=np.linspace(ind[0],ind[1],(ind[1]-ind[0])*10)
        A=(val[1]-val[0])/(ind[1]-ind[0])
        B=val[0]-A*ind[0]
        y=A*x + B
        ax[0].plot(x,y,'r')

    ax[0].grid()
    ax[0].plot(l,'k')

    #Divergence du rsi :

    for ind in Divergence_filtree :
        val=(l2[ind[0]],l2[ind[1]])
        x=np.linspace(ind[0],ind[1],(ind[1]-ind[0])*10)
        A=(val[1]-val[0])/(ind[1]-ind[0])
        B=val[0]-A*ind[0]
        y=A*x + B
        ax[1].plot(x,y,'b')

    ax[1].grid()
    ax[1].plot(l2,'k')
    ax[1].axhline(y=70,linestyle='-')
    ax[1].axhline(y=30,linestyle='-')
    ax[1].axhline(y=50,linestyle='-')
    ax[0].get_shared_x_axes().join(ax[0], ax[1])

    plt.show()

def BRTraceFinaux3(Divergence_filtree,l) :
    #### Tracés :
    fig, ax = plt.subplots(1,2, figsize=(8, 7))

    #Divergence_filtree=Filtration(Divergence)
    for ind in Divergence_filtree :
        Divergence_obj=Divergence_filtree(ind[0],ind[1])
        val=(l[ind[0]],l[ind[1]])
        x=np.linspace(ind[0],ind[1],(ind[1]-ind[0])*10)
        A=(val[1]-val[0])/(ind[1]-ind[0])
        B=val[0]-A*ind[0]
        y=A*x + B
        ax[0].text((ind[0]+ind[1])/2,(val[1]+val[0])/2,r'{}'.format(Divergence_obj.score))
        ax[0].plot(x,y,'r')

    ax[0].grid()
    ax[0].ylabel('Value of the asset ($)')
    ax[0].plot(l,'k')

    #Divergence du rsi :

    for ind in Divergence_filtree :
        val=(l2[ind[0]],l2[ind[1]])
        x=np.linspace(ind[0],ind[1],(ind[1]-ind[0])*10)
        A=(val[1]-val[0])/(ind[1]-ind[0])
        B=val[0]-A*ind[0]
        y=A*x + B
        ax[1].plot(x,y,'b')

    ax[1].grid()
    ax[1].ylabel('Value of the RSI')
    ax[1].plot(l2,'k')
    ax[1].axhline(y=70,linestyle='-')
    ax[1].axhline(y=30,linestyle='-')
    ax[1].axhline(y=50,linestyle='-')
    ax[0].get_shared_x_axes().join(ax[0], ax[1])

    plt.show()


