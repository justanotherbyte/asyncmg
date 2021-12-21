import asyncio
import json
from typing import (
    List,
    Optional,
    Tuple
)

from pymongo.uri_parser import parse_uri as _uriparse

from .node import Node


class ConnectionManager:
    OP_MSG = 2013
    OP_REPLY = 1
    OP_UPDATE = 2001
    OP_INSERT = 2002
    RESERVED = 2003
    OP_QUERY = 2004
    OP_GET_MORE = 2005
    OP_DELETE = 2006
    OP_KILL_CURSORS = 2007
    OP_COMPRESSED = 2012

    def __init__(self, uri: str):
        self.loop = asyncio.get_event_loop()

        self.uri = uri
        self.nodes: List[Node] = []
        self.connection_info = _uriparse(uri)
        
        self._attach_nodes(self.connection_info)

        self.reader: Optional[asyncio.StreamReader] = None
        self.writer: Optional[asyncio.StreamWriter] = None


    async def connect(self) -> Tuple[asyncio.StreamReader, asyncio.StreamWriter]:
        # we just grap the first Node
        node = self.nodes[0]
        reader, writer = await asyncio.open_connection(
            node.host,
            node.port,
            loop=self.loop
        )

        self.reader = reader
        self.writer = writer

        self.send({}, self.OP_INSERT)
        print(await self.read())

        return (reader, writer)

    def send(self, data):
        _bytes = json.dumps(data).encode()

        self.writer.write(_bytes)
    
    async def read(self, n: int = 1024) -> bytes:
        return await self.reader.read(n)

        
    def _attach_nodes(self, connection_info: dict):
        node_list = connection_info["nodelist"]
        if len(node_list) <= 0:
            raise ValueError("Node list is empty")

        username = connection_info["username"]
        password = connection_info["password"]

        for t in node_list:
            host, port = t

            node = Node(
                host,
                port,
                username,
                password
            )

            self.nodes.append(node)
