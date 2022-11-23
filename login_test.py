import asyncio
import unittest

from sgo import SGO


async def test_something():
    sgo = SGO()
    await sgo.get_homework()


if __name__ == '__main__':
    asyncio.run(test_something())
