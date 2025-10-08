from pymongo import MongoClient

from infrastructure.config.settings import Settings


class MongoConnection:
    _client: MongoClient = None
    _db = None

    def __init__(self, db_name: str):
        self.settings = Settings()
        self.db_name = db_name
        self.uri = self._build_uri()

    def connect(self):
        if self._client is None:
            self._client = MongoClient(self.uri)
            self._db = self._client[self.db_name]
        return self._client

    def _build_uri(self):
        user = self.settings.mongo_username
        password = self.settings.mongo_password
        host = self.settings.mongo_host
        port = self.settings.mongo_port
        auth_source = self.settings.mongo_auth_source or "admin"

        return f"mongodb://{user}:{password}@{host}:{port}/{self.db_name}?authSource={auth_source}"

    def get_db(self):
        if self._client is None:
            self.connect()
        if self._db is None:
            self._db = self._client[self.db_name]
        return self._db

    def close(self):
        if self._client:
            self._client.close()
            self._client = None
            self._db = None
