#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
from contextlib import AsyncExitStack

async def gestionCroupier(reader, writer):
    data = await reader.readline()
    print(data.decode())
    await writer.write(("Bienvenue sur le serveur blackjack").encode())

async def gestionJoueur(reader, writer):
    await writer.write(("Bienvenue joueur".encode()))


async def gestionnaire():
    croupiers = await asyncio.start_server(gestionCroupier, 'localhost', 668)
    print("Server on")
    async with croupiers:
        await croupiers.serve_forever() # handle requests for ever


if __name__ == "__main__":
    asyncio.run(gestionnaire())