class Node:
    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def as_dict(self) -> dict:
        return {
            "address": self.host,
            "port": self.port,
            "username": self.username,
            "password": self.password
        }

    def __repr__(self) -> str:
        fmt = "<Node host={0.host!r} port={0.port!r}>"
        return fmt.format(self)