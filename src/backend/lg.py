from services.langgraph.db import initialize_checkpointer, Saver


class LifespanMiddleware:
    async def __call__(self, scope, receive, send):
        if scope["type"] == "lifespan":
            while True:
                message = await receive()
                if message["type"] == "lifespan.startup":
                    # Startup logic
                    print("ASGI Startup: Pool ready")
                    await initialize_checkpointer()
                    await send({"type": "lifespan.startup.complete"})

                elif message["type"] == "lifespan.shutdown":
                    # Shutdown logic
                    print("ASGI Shutdown: Closing pool")
                    await Saver.pool.close()
                    await send({"type": "lifespan.shutdown.complete"})
                    return
