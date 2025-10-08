import logging

from fastapi import FastAPI

from domain.adapters.dependencies import lifespan
from presentation.routers.task_router import task_router


class Server:
    logger = logging.getLogger(__name__)

    def __init__(self, settings):
        self.app = FastAPI(lifespan=lifespan)
        self.settings = settings
        self.add_routers()

    def setups(self):
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    def get_server(self):
        return self.app

    def add_routers(self):
        self.app.include_router(task_router)
