import asyncio
from sys import argv

async def gestionCroupier(reader, writer):
    writer.write(("Bienvenue sur le serveur blackjack").encore())

async def gestionJoueur(reader, writer):
    writer.write(("Bienvenue joueur".encore()))


async def gestionnaire():
    joueurs = await asyncio.start_server(gestionJoueur, "0.0.0.0", 667)
    croupiers = await asyncio.start_server(gestionCroupier, "0.0.0.0", 668)
    async with AsyncExitStack() as stack:
        await stack.enter_async_context(s1)
        await stack.enter_async_context(s2)
        await asyncio.gather(
            s1.serve_forever(),
            s2.serve_forever(),
        )


if __name__ == "__main__":
    asyncio.run(gestionnaire())