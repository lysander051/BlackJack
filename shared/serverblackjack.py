#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
from sys import argv

async def gestionCroupier(reader, writer):
    data = await reader.read()
    print ("presque")
    writer.write(("Bienvenue sur le serveur blackjack").encode())

async def gestionJoueur(reader, writer):
    writer.write(("Bienvenue joueur".encode()))


async def gestionnaire():
    joueurs = await asyncio.start_server(gestionJoueur, '0.0.0.0', 667)
    croupiers = await asyncio.start_server(gestionCroupier, '0.0.0.0', 668)
    print("Server on")
    async with joueurs, croupiers:
        await asyncio.gather(
            joueurs.serve_forever(), croupiers.serve_forever())
        


if __name__ == "__main__":
    asyncio.run(gestionnaire())