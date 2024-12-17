import asyncio

def run_async(func, *args):
    return asyncio.run(func(*args))
