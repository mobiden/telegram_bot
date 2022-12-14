import asyncio
from asyncio import Task
from typing import Optional

from app.store import Store



class Poller:
    def __init__(self, store: Store):
        self.store = store
        self.is_running = False
        self.poll_task: Optional[Task] = None

    async def start(self):
        if self.store.admins.app.config.admin.debug:
            self.is_running = True
            self.poll_task = asyncio.create_task(self.poll())
        else:
            pass #TODO: change


    async def stop(self):
        if self.is_running and self.poll_task:
            self.is_running = False
            await self.poll_task

    async def poll(self):
        while self.is_running:
            if self.store.admins.app.config.admin.debug:
                await self.store.telegram_api.poll()

