#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import random
from sys import argv
'''  La liste des tables creees par le(s) croupier(s) '''
listeTable = []


''' Classe joueur general ou le joueur possede des cartes et un score'''
class JoueurGen : 
    ''' Initialisation d'un joueur general '''
    def __init__(self):
        self.cartes = []
        self.score = 0

    ''' Affichage d'une carte d'un joueur general ''' 
    def strCarte(self,carte):
        sortes=["coeur \u2764","carreau \u2726","pique \u2666","trefle \u2663"]
        plusDix=["V","D","R"]
        valeur=carte[0]
        if carte[0]>10 :
            valeur=plusDix[(carte[0]%10)-1]
        return "[   "+str(valeur) +"   " + sortes[carte[1]-1] + "  ]"

    ''' Affichage de toutes les cartes d'un joueur general '''
    def strToutCartes(self):
        s=""
        for carte in self.cartes:
            s+=self.strCarte(carte)+"   "
        return s

    ''' Calcul du score d'un joueur general avec V D R a 10 points et l'as peut compter 1 ou 11 '''
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

    '''Attribuer a score le score du joueur'''
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
        return "Carte du donneur= "+super().strCarte(self.cartes[0]) + " \n"

    ''' Affichage des cartes du donneur et son score lors de son tour'''
    def __strJeuFin__(self):
        return "Cartes du donneur= "+ super().__str__() 




''' Classe des joueurs '''
class Joueur(JoueurGen):

    ''' Initialisation d'un joueur qui a un attribut joue pour savoir s'il joue encore '''
    def __init__(self,writer):
        super().__init__()
        self.joue = True
        self.writer=writer

    ''' Affichage des cartes et du score d'un joueur'''
    def __str__(self):
        return "Vos cartes= "+ super().__str__()
   

    

''' Classe table '''
class Table:

    ''' Initialisation d'une table qui possede un nom de table, le temps d'attente, les joueurs, les cartes et le donneur'''
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

    ''' Donner une carte aleatoire a un joueur '''
    def donnercarte(self,j):
        carte = self.cartes.pop(random.randint(0,len(self.cartes)-1))
        j.cartes.append(carte)
        j.setScore()
       
    ''' Initialisation d'une partie en fabriquant les cartes et en distribuant 2 a chaque joueur'''
    def initialisationPartie(self):
        if self.cartes==[]:
            self.initialisationCarte()
            for i in range(2):
                self.donnercarte(self.donneur)
                for x in self.joueurs:
                    self.donnercarte(x)

    ''' Affichage d'une table : son nom et son temps d'attente '''
    def __str__(self):
        return "Nom = " + str(self.nom) + " | temps = " + str(self.temps)

    ''' Pour savoir s'il y a encore des joueurs qui jouent '''
    def joueurQuiJoue(self):
        for j in self.joueurs:
            if j.joue:
                return True
        return False



''' Quand le joueur e d'arreter de jouer ou bien quand il depasse 21 points '''
def resultatjoueur(joueur,writer):
    if(joueur.score>21):
        writer.write("Vous depassez 21, c'est fini! Vous avez perdu.\n".encode())
    elif(joueur.score<21):
        s="Vous etes a " + str(joueur.score) + ", avec un peu de chance vous allez gagner, on attend le tour du donneur.\n"
        writer.write(s.encode())
    else:
        s= "Vous avez 21 on n'attend plus que le donneur.\n" 
        writer.write(s.encode())


''' Parcourir la liste des tables pour savoir a quelle table le joueur va jouer'''
def parcourTable(table):
    for x in listeTable:
        if x.nom == table:
            return x
    return None


''' En attente des joueurs qui viennent a la table pour jouer '''
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
        else :
            table.donnercarte(joueur)
            writer.write((str(joueur)).encode())
            
        
        if joueur.score>21 :
            resultatjoueur(joueur,writer)
            joueur.joue=False
            writer.write(("END\n").encode())
        if joueur.score<=21 and suite!=0 :
            writer.write((".\n").encode())

    await finPartie(table)
    
    if(table.donneur.score >21 or table.donneur.score < joueur.score):
        writer.write(("Vous avez gagne.\n").encode())
    elif(table.donneur.score > joueur.score) :
        writer.write(("Le donneur a gagne.\n").encode())
    else:
        writer.write(("Vous etes a egalite.\n").encode())
 
    writer.write(("END\n").encode())
   

''' Envoie un message a chaque joueur '''
def affichagePourChaqueJoueur(table,msg):
    for x in table.joueurs:
        x.writer.write(msg.encode())


''' Le donneur joue : il prend une carte tant qu'il est en dessous de 17 '''
def tourDuDonneur(table):
    donneur=table.donneur
    affichagePourChaqueJoueur(table,donneur.__strJeuFin__())
        
    while donneur.score<17:
        table.donnercarte(donneur)
        affichagePourChaqueJoueur(table,donneur.__strJeuFin__())


''' Faire patienter les autres joueurs qui ont fini de jouer tant qu'il y a des joueurs qui n'ont pas fini de jouer'''
async def finPartie(table) : 
    if(table.joueurQuiJoue()):
        while table.joueurQuiJoue():
            await asyncio.sleep(1)
    else:
        tourDuDonneur(table)


''' Renvoie la reponse des joueurs selon les commandes fournies au bon forma'''
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


''' Creer un croupier et une table avec la duree d'attente pour pouvoir commencer a jouer sur cette table '''
async def gestionCroupier(reader, writer):
    writer.write(("Bienvenue croupier.\n").encode())

    nomTable = commandes((await reader.readline()).decode())
    t = Table(nomTable)
    writer.write(("Le nom de la table est: " + t.nom + ".\n").encode())

    temps = commandes((await reader.readline()).decode())
    t.temps = temps
    writer.write(("La duree de la table est: " + str(t.temps) + ".\n").encode())
    listeTable.append(t)


''' Creer un joueur, demande a quelle table il veut jouer et commencer la partie '''
async def gestionJoueur(reader, writer):
    writer.write(("Bienvenue joueur.\n").encode())

    nomTable = commandes((await reader.readline()).decode())
    table = parcourTable(nomTable)
    if table == None or table.temps <= 0:
        writer.write("END\n".encode())
        return
    joueur = Joueur(writer)
    table.joueurs.append(joueur)

    await attenteTable(table)

    table.initialisationPartie()
    writer.write((str(joueur)).encode())
    writer.write((str(table.donneur)).encode())

    await partie(reader,writer,joueur,table)
    if parcourTable(table.nom)!=None:
        listeTable.remove(table)


''' Permet d'ouvrir une session pour les joueurs ou les croupiers '''
async def gestionnaire():
    joueurs = await asyncio.start_server(gestionJoueur, '0.0.0.0', 667)
    croupiers = await asyncio.start_server(gestionCroupier, '0.0.0.0', 668)
    async with joueurs, croupiers:
        await asyncio.gather(
            joueurs.serve_forever(), croupiers.serve_forever())
        

if __name__ == "__main__":
    asyncio.run(gestionnaire())
