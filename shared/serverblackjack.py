#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import random
from sys import argv
'''  La liste des tables creees par le(s) croupier(s) '''
listeTable = []


''' Classe joueur general où le joueur possède des cartes et un score'''
class JoueurGen : 
    ''' Initialisation d'un joueur général '''
    def __init__(self):
        self.cartes = []
        self.score = 0

    ''' Affichage d'une carte d'un joueur général ''' 
    def strCarte(self,carte):
        
        #sorte=["\u2764","\u2726","\u2663","\u2666"]
        sortes=["coeur","carreau","pique","trefle"]
        plusDix=["V","D","R"]
        valeur=carte[0]
        if carte[0]>10 :
            valeur=plusDix[(carte[0]%10)-1]
        #return str(valeur,sorte[carte[1]-1]))
        return "[   "+str(valeur) +"   " + sortes[carte[1]-1] + "  ]"

    ''' Affichage de toutes les cartes d'un joueur général '''
    def strToutCartes(self):
        s=""
        for carte in self.cartes:
            s+=self.strCarte(carte)+"   "
        return s

    ''' Calcul du score d'un joueur général avec V D R à 10 points et l'as peut compter 1 ou 11 '''
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
        if nombreAs>0 and (s-1)<=10:
            s+=10
        return s

    '''Attribuer à score le score du joueur'''
    def setScore(self):
        self.score=self.calculeScore()

    ''' Affichage des cartes et du score d'un joueur classique '''
    def __str__(self):
        return self.strToutCartes() +" | score= "+ str(self.score) + "\n"

    
    
    
''' Celui qui partage les cartes et aussi l'adversaire des joueurs '''
class Donneur(JoueurGen):

    def __init__(self):
        super().__init__()

    ''' Affichage d'une carte du donneur avec le score correspondant, pour montrer aux joueurs sa 1ere carte'''
    def __str__(self):
        return "carte du donneur= "+super().strCarte(self.cartes[0]) + " \n"

    ''' Affichage des cartes du donneur et son score lors de son tour'''
    def __strJeuFin__(self):
        return "carte du donneur= "+ super().__str__() 




''' Classe des joueurs '''
class Joueur(JoueurGen):

    ''' Initialisation d'un joueur qui a un attribut joue pour savoir s'il joue encore '''
    def __init__(self):
        super().__init__()
        self.joue = True

    ''' Affichage des cartes et du score d'un joueur'''
    def __str__(self):
        return "vos cartes= "+ super().__str__()
   

    

''' Classe table '''
class Table:

    ''' Initialisation d'une table qui possède un nom de table, le temps d'attente, les joueurs, les cartes et le donneur'''
    def __init__(self, nom):
        self.nom = nom
        self.temps = 0
        self.joueurs = []
        self.cartes = []
        self.donneur = Donneur()

    ''' Fabrication des 52 cartes '''
    def initialisationCarte(self):
        for i in range (1,5):
            for j in range(1,14):
                self.cartes.append((j,i))

    ''' Donner une carte aleatoire à un joueur '''
    def donnercarte(self,j):
        carte = self.cartes.pop(random.randint(0,len(self.cartes)-1))
        j.cartes.append(carte)
        j.setScore()
       
    ''' Initialisation d'une partie en fabriquant les cartes et en distribuant 2 à chaque joueur'''
    def initialisationPartie(self):
        if self.cartes==[]:
            self.initialisationCarte()
            print(self.cartes)
            for i in range(2):
                #carte = self.cartes.pop(random.randint(0,len(self.cartes)-1))
                self.donnercarte(self.donneur)
                #self.donneur.setScore()
                #self.donneur.cartes.append(carte)
                #self.donneur.score+=carte[0]
                for x in self.joueurs:
                    self.donnercarte(x)
                    #x.setScore()
                    print(self.donneur)

    ''' Affichage d'une table : son nom et son temps d'attente '''
    def __str__(self):
        return "nom = " + str(self.nom) + " | temps = " + str(self.temps)

    ''' Pour savoir s'il y a encore des joueurs qui jouent '''
    def joueurQuiJoue(self):
        for j in self.joueurs:
            if j.joue:
                return True
        return False

    
    

''' Quand le joueur décide d'arreter de jouer ou bien quand il dépasse 21 points '''
def resultatjoueur(joueur,writer):
    if(joueur.score>21):
        writer.write("vous depassez 21 c'est fini\n".encode())
    elif(joueur.score<21):
        s="vous etes à " + str(joueur.score) + " avec un peu de chance vous allez gagner\n"
        writer.write(s.encode())
    else:
        s= "vous avez 21 on n'attend plus que le donneur\n" 
        writer.write(s.encode())

''' Fonction de parcour des joueurs '''
def parcourJoueurs(table, joueur):
    for x in table.joueurs:
        if x.id[0] == joueur.id[0]:
            return x
    return None

''' Parcourir la liste des tables pour savoir à quelle table le joueur va jouer'''
def parcourTable(table):
    for x in listeTable:
        if x.nom == table:
            return x
    return None

''' En attente des joueurs qui viennent à la table pour jouer '''
async def attenteTable(table):
    while 0 <= table.temps :
        await asyncio.sleep(1)
        table.temps-=1

''' Gestion d'une partie entre joueur et donneur sur une table '''
async def partie(reader, writer,joueur,table):
    writer.write(".\n".encode())
    while(joueur.joue):
        suite = commandes((await reader.readline()).decode())
        if suite == 0 :
            resultatjoueur(joueur,writer)
            writer.write((str(joueur)).encode())
            joueur.joue=False
            #joueur.score=joueur.calculeScore()
        else :
            table.donnercarte(joueur)
            writer.write((str(joueur)).encode())
            
        #joueur.setScore()
        if joueur.score>21 :
            resultatjoueur(joueur,writer)
            joueur.joue=False
            writer.write(("END\n").encode())
        if joueur.score<=21 and suite!=0 :
            writer.write((".\n").encode())

    await finPartie(table)
    donneur=table.donneur
    writer.write((donneur.__strJeuFin__()).encode())
    while donneur.score<17:
        table.donnercarte(donneur)
        #donneur.setScore()
        writer.write((donneur.__strJeuFin__()).encode())

    if(donneur.score >21 or donneur.score < joueur.score):
        writer.write(("Vous avez gagné\n").encode())
    elif(donneur.score > joueur.score) :
        writer.write(("Le donneur a gagné\n").encode())
    else:
        writer.write(("Vous êtes à égalité\n").encode())
 
    writer.write(("END\n").encode())
    

''' Faire patienter les autres joueurs qui ont fini de jouer tant qu'il y a des joueurs qui n'ont pas fini de jouer'''
async def finPartie(table) : 
    while table.joueurQuiJoue():
        await asyncio.sleep(1)


''' Renvoie la réponse des joueurs selon les commandes fournies au bon forma'''
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


''' Créer un croupier et une table avec la durée d'attente pour pouvoir commencer à jouer sur cette table '''
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


''' Créer un joueur, demande à quelle table il veut jouer et commencer la partie '''
async def gestionJoueur(reader, writer):
    print("un joueur c'est connecte")
    writer.write(("Bienvenue joueur\n").encode())

    nomTable = commandes((await reader.readline()).decode())
    table = parcourTable(nomTable)
    if table == None or table.temps <= 0:
        writer.write("END\n".encode())
        return
    print(writer.get_extra_info('peername'))
    joueur = Joueur()
    table.joueurs.append(joueur)
    print("joueur ajoute a table: " + str(table.nom))

    await attenteTable(table)

    table.initialisationPartie()
    writer.write((str(joueur)).encode())
    writer.write((str(table.donneur)).encode())

    await partie(reader,writer,joueur,table)


''' Permet d'ouvrir une session pour les joueurs ou les croupiers '''
async def gestionnaire():
    joueurs = await asyncio.start_server(gestionJoueur, '0.0.0.0', 667)
    croupiers = await asyncio.start_server(gestionCroupier, '0.0.0.0', 668)
    print("Server on")
    async with joueurs, croupiers:
        await asyncio.gather(
            joueurs.serve_forever(), croupiers.serve_forever())
        

if __name__ == "__main__":
    asyncio.run(gestionnaire())
