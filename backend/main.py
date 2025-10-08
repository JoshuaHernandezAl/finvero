from infrastructure.config.init_server import Server
from infrastructure.config.settings import Settings


app = Server(Settings()).get_server()
