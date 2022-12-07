import asyncio
import logging

import bot.telegram_bot
from notifications.api import Api
from notifications.notifications import scan_new_grades
from sgo import SGO

sgo = SGO()

logging.basicConfig(level=logging.INFO)


async def observe_homework():
    logging.info("bot: init")
    while True:
        try:
            logging.info("bot: get homework")
            await sgo.get_homework()
            logging.info("bot: collected")
        except Exception as e:
            print(e)
        finally:
            await asyncio.sleep(1800)


async def observe_new_grades():
    logging.info("notifications: init")
    api = Api()
    while True:
        try:
            users = api.get_all_users()
            for user in users:
                logging.info(f"notifications: scan user {user.user_id}")
                await scan_new_grades(api, user)
                await asyncio.sleep(5)
        except Exception as e:
            logging.error(e)
        finally:
            await asyncio.sleep(600)


if __name__ == '__main__':
    ioloop = asyncio.new_event_loop()
    tasks = [
        ioloop.create_task(bot.telegram_bot.run()),
        ioloop.create_task(observe_homework()),
        ioloop.create_task(observe_new_grades())
    ]

    ioloop.run_forever()
