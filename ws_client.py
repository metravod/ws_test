import json
import time
import logging
from websocket import create_connection

from settings import ws_uri, chunk_size

logger = logging.getLogger('ws_client')


# Подключение к вебсокету
ws = create_connection(ws_uri)


def key_for_sort(dictionary: dict) -> int:
    return dictionary['id']


# В бесконечном цикле наполняем список до 100 элементов
# потом сортируем его
while True:
    chunk_recv = []
    ts = time.time()
    while len(chunk_recv) < chunk_size:
        result = json.loads(ws.recv())
        chunk_recv.append(result)
    tc = time.time()
    chunk_recv.sort(key=key_for_sort)
    te = time.time()
    logger.warning(f'new chunk - forming {tc - ts} - sort {te - tc} -> {len(chunk_recv)}')
