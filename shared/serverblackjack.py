#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
from contextlib import AsyncExitStack

async def gestionCroupier(reader, writer):
    await data = reader.readline()
    print(data.decode())
    await writer.write(("Bienvenue sur le serveur blackjack").encode())

async def gestionJoueur(reader, writer):
    await writer.write(("Bienvenue joueur".encode()))


async def gestionnaire():
    joueurs = await asyncio.start_server(gestionJoueur, 'localhost', 667)
    croupiers = await asyncio.start_server(gestionCroupier, 'localhost', 668)
    print("Server on")
    async with AsyncExitStack() as stack:
        await stack.enter_async_context(joueurs)
        await stack.enter_async_context(croupiers)
        await asyncio.gather(
            joueurs.serve_forever(),
            croupiers.serve_forever(),
        )


if __name__ == "__main__":
    asyncio.run(gestionnaire())