import asyncio
import unittest

from sgo import SGO


async def test_something():
    sgo = SGO()
    print(await sgo.get_parent_info_letter())


if __name__ == '__main__':
    asyncio.run(test_something())
