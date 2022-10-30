#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
from sys import argv

class Table:
    def __init__(self, table):
        self.table = table

    def __str__(self):
        return "nom de la table = " + str(self.table)

async def gestionCroupier(reader, writer):
    print("Un croupiers creait une table")
    writer.write(("Bienvenue croupier\n").encode())
    table = await reader.readline()
    t = Table(table.decode())
    print(t)


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