#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import random
from sys import argv

listeTable = []

class Donneur:
    def __init__(self):
        self.cartes = []
        self.score = 0

    def __str__(self):
        return "carte du donneur= "+str(self.cartes[0])+" | son score= "+ str(self.cartes[0][0]) + "\n"

class Joueur:
    def __init__(self, id, reader, writer):
        self.id = id
        self.reader = reader
        self.writer = writer
        self.cartes = []
        self.score = 0
        self.joue = True

    def __str__(self):
        return "vos cartes= "+str(self.cartes)+" | votre score= "+ str(self.score) + "\n"

class Table:
    def __init__(self, nom):
        self.nom = nom
        self.temps = 0
        self.joueurs = []
        self.cartes = []
        self.donneur = Donneur()

    def initialisationCarte(self):
        for i in range (1,5):
            for j in range(1,14):
                self.cartes.append((j,i))

    def initialisationPartie(self):
        if self.cartes==[]:
            self.initialisationCarte()
            print(self.cartes)
            for i in range(2):
                carte = self.cartes.pop(random.randint(0,len(self.cartes)-1))
                self.donneur.cartes.append(carte)
                self.donneur.score+=carte[0]
                for x in self.joueurs:
                    carte = self.cartes.pop(random.randint(0,len(self.cartes)-1))
                    x.cartes.append(carte)
                    x.score+=carte[0]
                    print(self.donneur)

    def __str__(self):
        return "nom = " + str(self.nom) + " | temps = " + str(self.temps)

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

def partie(reader, writer):
    writer.write(".\n".encode())

def commandes(com):
    prefix = com.split()
    if prefix[0] == "NAME":
        return prefix[1]
    elif prefix[0] == "TIME":
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
    print("joueur ajoute a table: " + str(table.nom))

    await attenteTable(table)

    table.initialisationPartie()
    writer.write((str(joueur)).encode())
    writer.write((str(table.donneur)).encode())

    partie(reader,writer)


async def gestionnaire():
    joueurs = await asyncio.start_server(gestionJoueur, '0.0.0.0', 667)
    croupiers = await asyncio.start_server(gestionCroupier, '0.0.0.0', 668)
    print("Server on")
    async with joueurs, croupiers:
        await asyncio.gather(
            joueurs.serve_forever(), croupiers.serve_forever())
        

if __name__ == "__main__":
    asyncio.run(gestionnaire())