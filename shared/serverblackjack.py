#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
from sys import argv

class Table:
    def __init__(self, table, temps=60):
        self.table = table
        self.temps = temps

    def __str__(self):
        return "nom = " + str(self.table) + " | temps = " + self.temps


def commandes(com):
    prefix = com.split()
    if prefix[0] == "NAME":
        return prefix[1]
    elif prefix[0] == "TIME":
        return prefix[1]
    else:
        return "erreur"

async def gestionCroupier(reader, writer):
    print("Un croupiers creait une table")
    writer.write(("Bienvenue croupier\n").encode())

    table = commandes((await reader.readline()).decode())
    t = Table(table)
    print(t)
    writer.write(("Le nom de la table est:" + t.table + " \n").encode())

    temps = commandes((await reader.readline()).decode())
    t = Table(temps)
    print(t)
    writer.write(("la duree de la table est:" + t.temps + " \n").encode())

async def gestionJoueur(reader, writer):
    writer.write(("Bienvenue joueur\n".encode()))


async def gestionnaire():
    joueurs = await asyncio.start_server(gestionJoueur, '0.0.0.0', 667)
    croupiers = await asyncio.start_server(gestionCroupier, '0.0.0.0', 668)
    print("Server on")
    async with joueurs, croupiers:
        await asyncio.gather(
            joueurs.serve_forever(), croupiers.serve_forever())
        


if __name__ == "__main__":
    asyncio.run(gestionnaire())