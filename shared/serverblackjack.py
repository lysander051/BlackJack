#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
from sys import argv

async def gestionCroupier(reader, writer):
    print ("presque")
    await writer.write(("Bienvenue sur le serveur blackjack").encode())

async def gestionJoueur(reader, writer):
    writer.write(("Bienvenue joueur".encode()))


async def gestionnaire():
    croupiers = await asyncio.start_server(gestionCroupier, '0.0.0.0', 668)
    print("Server on")
    async with croupiers:
        await croupiers.serve_forever()
        


if __name__ == "__main__":
    asyncio.run(gestionnaire())