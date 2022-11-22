#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import random
from sys import argv

listeTable = []



class JoueurGen : 
    def __init__(self):
        self.cartes = []
        self.score = 0

    def strCarte(self,carte):
        sorte=["coeur","pique","trefle","carreau"]
        plusDix=["V","D","R"]
        valeur=str(carte[0])
        if carte[0]>10 :
            valeur=plusDix[(carte[0]%10)-1]
        return str((valeur,sorte[carte[1]-1]))

    def strToutCartes(self):
        s=""
        for carte in self.cartes:
            s+=self.strCarte(carte)+"  "
        return s

    def calculeScore(self):
        s=0
        nombreAs=0
        for carte in self.cartes:
            if carte[0]>10:
                s+=10
            else:
                if carte[0]==1 :
                    nombreAs+=1
            
                s+=carte[0]
        if nombreAs>0 & s-1<=10:
            s+=10
        return s


        


    '''def strCartes(self):
        sorte=["coeur","pique","trefle","carreau"]
        plusDix=["V","D","R"]
        s=""
        for carte in self.cartes:
            valeur=str(carte[0])
            if carte[0]>10 :
                valeur=plusDix[(carte[0]%10)-1]
            s+=str((valeur,sorte[carte[1]-1]))+ "     "
        return s'''

 

    def __str__(self):
        #stpl = self.affichageCarte() 
        #print(stpl)
        #return "vos cartes= "+str(self.cartes)+" | votre score= "+ str(self.score) + "\n"
        #return "vos cartes= "+ stpl +" | votre score= "+ str(self.score) + "\n"
        return "vos cartes= "+ self.strToutCartes() +" | votre score= "+ str(self.calculeScore()) + "\n"

    
        

    

class Donneur(JoueurGen):
    def __init__(self):
        super().__init__()


    def __str__(self):
        return "carte du donneur= "+super().strCarte(self.cartes[0]) + "\n"
        #+" | son score= "+ str(self.cartes[0][0]) + "\n"

class Joueur(JoueurGen):
    def __init__(self, id, reader, writer):
        super().__init__()
        self.id = id
        self.reader = reader
        self.writer = writer
        self.joue = True

    
        #return "vos cartes= "+str(self.cartes)+" | votre score= "+ str(self.score) + "\n"

# heritage joueur ( donneur et joueur) 
# fonction affichage carte joueur general
# fonction score joueur general

class Table:
    def __init__(self, nom):
        self.nom = nom
        self.temps = 0
        self.joueurs = []
        self.cartes = []
        self.donneur = Donneur()
        self.joueursJouer = []

    def initialisationCarte(self):
        for i in range (1,5):
            for j in range(1,14):
                self.cartes.append((j,i))
    def donnercarte(self,joueur):
        carte = self.cartes.pop(random.randint(0,len(self.cartes)-1))
        joueur.cartes.append(carte)
       

    def initialisationPartie(self):
        if self.cartes==[]:
            self.initialisationCarte()
            print(self.cartes)
            for i in range(2):
                carte = self.cartes.pop(random.randint(0,len(self.cartes)-1))
                self.donneur.cartes.append(carte)
                self.donneur.score+=carte[0]
                for x in self.joueurs:
                    #carte = self.cartes.pop(random.randint(0,len(self.cartes)-1))
                    x.cartes.append(self.donnercarte())
                    #x.score+=carte[0]
                    print(self.donneur)

    def __str__(self):
        return "nom = " + str(self.nom) + " | temps = " + str(self.temps)

    def joueurQuiJoue(self):
        for j in self.joueurs:
            if j.joue:
                return True
        return False

def resultatjoueur(joueur):
    if(joueur.calculeScore()>21):
        writer.write("vous depassez 21 c'est fini\n".encode())
    else if(joueur.calculeScore()<21):
        s="vous ete à " + str(joueur.calculeScore()) + " avec un peu de chance vous allez gagner\n"
         writer.write(s.encode())
    else:
        s= "vous avez 21 on n'attend plus que le donneur\n" 
        writer.write(s.encode())




def parcourJoueurs(table, joueur):
    for x in table.joueurs:
        if x.id[0] == joueur.id[0]:
            return x
    return None

def parcourTable(table):
    for x in listeTable:
        if x.nom == table:
            return x
    return None

async def attenteTable(table):
    while 0 <= table.temps :
        await asyncio.sleep(1)
        table.temps-=1

async def partie(reader, writer,joueur,table):
    writer.write(".\n".encode())
        while(joueur.joue):
            suite = commandes((await reader.readline()).decode())
            if suite == 0 :
                joueur.resultatjoueur()
                writer.write((str(j)).encode())
                joueur.joue=false
                joueur.score=joueur.calculeScore()
            else :
                table.donnercarte(joueur)
                writer.write((str(joueur)).encode())
                writer.write((".\n").encode())
            if joueur.calculeScore()>21 :
                joueur.resultatjoueur()
                joueur.joue=false
                joueur.score=joueur.calculeScore()
                writer.write(("END\n").encode())


    await finPartie()

    donneur=table.donneur
    writer.write((str(donneur)).encode())

    while donneur.calculeScore()<17:
        writer.write(".").encode()
        writer.write("1").encode()
        table.donnercarte(donneur)
        writer.write((str(donneur)).encode())

    donneur.score=donneur.calculeScore

    if(donneur.score> joueur.score) :
        writer.write("Le donneur a gagné")
    else if( donneur.score ==  joueur.score):
        writer.write("Exeaquo")
    else : 
        writer.write("Vous avez gagné")
    
    writer.write(("END\n").encode())
    

       
   # suite = commandes((await reader.readline()).decode())





async def finPartie(table) : 
    while table.joueurQuiJoue():
        asyncio.sleep(1)
        

               
    
    






    


def commandes(com):
    prefix = com.split()
    if prefix[0] == "NAME":
        return prefix[1]
    elif prefix[0] == "TIME":
        return int(prefix[1])
    elif prefix[0] == "MORE":
        return int(prefix[1])
    else:
        return "erreur"

async def gestionCroupier(reader, writer):
    print("Un croupiers creait une table")
    writer.write(("Bienvenue croupier\n").encode())

    nomTable = commandes((await reader.readline()).decode())
    t = Table(nomTable)
    print(t)
    writer.write(("Le nom de la table est:" + t.nom + " \n").encode())

    temps = commandes((await reader.readline()).decode())
    t.temps = temps
    print(t)
    writer.write(("la duree de la table est:" + str(t.temps) + " \n").encode())
    listeTable.append(t)


async def gestionJoueur(reader, writer):
    print("un joueur c'est connecte")
    writer.write(("Bienvenue joueur\n").encode())

    nomTable = commandes((await reader.readline()).decode())
    table = parcourTable(nomTable)
    if table == None or table.temps <= 0:
        writer.write("END\n".encode())
        return

    joueur = Joueur(writer.get_extra_info('peername'), reader, writer)
    table.joueurs.append(joueur)
    table.joueursJouer.append(joueur)
    print("joueur ajoute a table: " + str(table.nom))

    await attenteTable(table)

    table.initialisationPartie()
    writer.write((str(joueur)).encode())
    writer.write((str(table.donneur)).encode())

    partie(reader,writer,joueur,table)


async def gestionnaire():
    joueurs = await asyncio.start_server(gestionJoueur, '0.0.0.0', 667)
    croupiers = await asyncio.start_server(gestionCroupier, '0.0.0.0', 668)
    print("Server on")
    async with joueurs, croupiers:
        await asyncio.gather(
            joueurs.serve_forever(), croupiers.serve_forever())
        

if __name__ == "__main__":
    asyncio.run(gestionnaire())