#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
from contextlib import AsyncExitStack

async def gestionCroupier(reader, writer):
    writer.write(("Bienvenue sur le serveur blackjack").encode())

async def gestionJoueur(reader, writer):
    writer.write(("Bienvenue joueur".encode()))


async def gestionnaire():
    joueurs = await asyncio.start_server(gestionJoueur, 'localhost', 667)
    croupiers = await asyncio.start_server(gestionCroupier, 'localhost', 668)
    async with AsyncExitStack() as stack:
        await stack.enter_async_context(s1)
        await stack.enter_async_context(s2)
        await asyncio.gather(
            s1.serve_forever(),
            s2.serve_forever(),
        )


if __name__ == "__main__":
    asyncio.run(gestionnaire())