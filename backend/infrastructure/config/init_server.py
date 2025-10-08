import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from domain.adapters.dependencies import lifespan
from presentation.routers.task_router import task_router


class Server:
    logger = logging.getLogger(__name__)

    def __init__(self, settings):
        self.app = FastAPI(lifespan=lifespan)
        self.settings = settings
        self.add_routers()
        self.setups()

    def setups(self):
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def get_server(self):
        return self.app

    def add_routers(self):
        self.app.include_router(task_router)
