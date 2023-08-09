import json
import asyncio
import time
import logging
from operator import itemgetter

from websocket import create_connection

from settings import ws_uri_receive, ws_uri_send, test_chunk_size, key_for_sort

logging.basicConfig(filename='msg_sort.log', level=logging.INFO)
logger = logging.getLogger('ws_client')


class WsMessageSorter:
    """
    Сортировщик сообщений.
    Получает с одного вебсокета сообщения в режиме реального времени,
    собирает их в chunk заданного размера, сортирует по нужному полю,
    и отправляет в другой вебсокет.

    Arguments
    ---------
    uri_receive: str
        uri вебсокета, с которого необходимо читать сообщения
    uri_send: str
        uri вебсокета, на который необходимо отправлять отсортированные сообщения
    chunk_size: int
        сколько входящего сообщений необходимо объединить для последующей сортировки

    Methods
    -------
    run
        Запуск сортировщика сообщений
    """

    def __init__(self, uri_receive: str, uri_send: str, chunk_size: int, key_for_sort: str):
        self.uri_receive = uri_receive
        self.uri_send = uri_send
        self.chunk_size = chunk_size
        self.key_for_sort = key_for_sort

    async def run(self) -> None:
        self._create_connections()
        while True:
            await self._get_chunk()
            await self._sort_chunk()
            await self._send_chunk()
            await self._write_logs()

    def _create_connections(self) -> None:
        """Создаем подключения к вебсокетам, на получение и на отправку"""
        self._ws_receive = create_connection(self.uri_receive)
        self._ws_send = create_connection(self.uri_send)

    async def _get_chunk(self) -> None:
        """Собираем chunk из входящих сообщений, заданного размера"""
        self._time_start_chunk = time.time()
        self._chunk = []
        while len(self._chunk) < self.chunk_size:
            res = json.loads(self._ws_receive.recv())
            self._chunk.append(res)
        self._time_end_chunk = time.time()

    async def _sort_chunk(self) -> None:
        """Сортируем получившийся chunk по заданному ключевому полю"""
        self._chunk.sort(key=itemgetter(self.key_for_sort))

    async def _send_chunk(self) -> None:
        """Отправляем отсортированный chunk"""
        self._ws_send.send(json.dumps(self._chunk))
        self._time_send_chunk = time.time()

    async def _write_logs(self) -> None:
        """Считаем время работы и пишем в логи"""
        time_collect_chunk = round(self._time_end_chunk - self._time_start_chunk, 5)
        time_from_collect_to_sent = round(self._time_send_chunk - self._time_end_chunk, 5)
        logger.info(f'chunk sent: collect - {time_collect_chunk} sec, sort&send - {time_from_collect_to_sent} sec')


if __name__ == '__main__':
    mesage_sorter = WsMessageSorter(
        uri_receive=ws_uri_receive,
        uri_send=ws_uri_send,
        chunk_size=test_chunk_size,
        key_for_sort=key_for_sort
    )
    loop = asyncio.get_event_loop()
    loop.run_until_complete(mesage_sorter.run())
