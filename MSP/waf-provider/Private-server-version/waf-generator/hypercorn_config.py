import asyncio
import hypercorn.asyncio
import hypercorn.config
from server import server

def run_server():
    config = hypercorn.config.Config()
    config.bind = ["0.0.0.0:5000"]
    asyncio.run(hypercorn.asyncio.serve(server, config))

if __name__ == '__main__':
    run_server()