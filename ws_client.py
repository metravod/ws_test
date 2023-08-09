import json
from typing import Any
from websocket import create_connection

from settings import ws_uri_receive, ws_uri_send, chunk_size
from timeit import timeit


class WsOrderedMessages:

    def __init__(self, uri_receive: str, uri_send: str, chunk_size: int):
        self.uri_receive = uri_receive
        self.uri_send = uri_send
        self.chunk_size = chunk_size
        self.key_for_sort = 'id'

    def run(self) -> None:
        self._ws_receive = self._create_conn(self.uri_receive)
        self._ws_release = self._create_conn(self.uri_send)
        while True:
            self._get_chunk()
            self._sort_chunk()
            self._send_chunk()

    @staticmethod
    def _create_conn(uri: str) -> Any:
        # Подключение к вебсокету
        return create_connection(uri)

    @timeit
    def _get_chunk(self) -> None:
        self._chunk = []
        while len(self._chunk) < self.chunk_size:
            res = json.loads(self._ws_receive.recv())
            self._chunk.append(res)

    @timeit
    def _sort_chunk(self) -> None:
        self._chunk.sort(key=lambda dictionary: dictionary[self.key_for_sort])

    @timeit
    def _send_chunk(self) -> None:
        self._ws_release.send(json.dumps(self._chunk))


if __name__ == '__main__':
    WsOrderedMessages(ws_uri_receive, ws_uri_send, chunk_size).run()
