import csv
from django.core.management.base import BaseCommand

import asyncio
import aiohttp
from collections import deque
from time import time
from .db_fns import truncate_phone_table, insert_csvblob


async def fetch_reestr(url, session: aiohttp.ClientSession):
    async with session.get(url, allow_redirects=True) as responce:
        data = await responce.read()
        data = csv.reader(data.decode('utf-8').splitlines(), delimiter=';')
        insert_csvblob(data)


async def update_reestr():
    reestr_urls = [
        'https://rossvyaz.ru/data/ABC-3xx.csv',
        'https://rossvyaz.ru/data/ABC-4xx.csv',
        'https://rossvyaz.ru/data/ABC-8xx.csv',
        'https://rossvyaz.ru/data/DEF-9xx.csv'
    ]

    q = deque()

    async with aiohttp.ClientSession() as session:
        for r in reestr_urls:
            q.append(asyncio.create_task(fetch_reestr(r, session)))
        await asyncio.gather(*q)


def renew_reestr():
    t0 = time()
    truncate_phone_table()
    asyncio.run(update_reestr())
    print(f'реестр обновлен,за {time() - t0} секунд')

    pass


class Command(BaseCommand):
    def handle(self, **options):
        try:
            renew_reestr()
        except:
            print('exception was raised')
            return
        finally:
            print('update_db done')
