import logging
import os

from models.event.event_model import EventModel
from services.string.string_service import StringService


class EventFolderService:
    event: EventModel

    def __init__(self, event: EventModel) -> None:
        self.event = event

    @staticmethod
    def get_data_folder() -> str:
        return "/code/data"

    def get_event_folder(self) -> str:
        sanitized_name = StringService.sanitize(self.event.name)

        return f"{self.get_data_folder()}/{self.event.event_code}_{sanitized_name}"

    def create_event_folder_if_not_exists(self) -> None:
        event_folder = self.get_event_folder()
        logging.debug(f"Creating event path {event_folder}...")
        os.makedirs(name=event_folder, exist_ok=True)

        files_folder = os.path.join(event_folder, "arquivos")
        logging.debug(f"Creating files path {files_folder}...")
        os.makedirs(name=files_folder, exist_ok=True)
