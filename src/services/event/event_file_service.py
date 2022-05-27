import logging
import os

from models.event.event_model import EventModel
from models.file.file_model import FileModel
from services.event.event_folder_service import EventFolderService
from services.http.http_service import HttpService
from services.string.string_service import StringService


class EventFileService:
    event: EventModel
    file: FileModel

    def __init__(self, event: EventModel, file: FileModel) -> None:
        self.event = event
        self.file = file

    @staticmethod
    def get_request_headers() -> dict:
        return {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }

    def download(self) -> None:
        folder_service = EventFolderService(event=self.event)
        folder_service.create_event_folder_if_not_exists()

        folder_path = folder_service.get_event_folder()
        files_folder_path = os.path.join(folder_path, "arquivos")

        full_file_url = f"https://cscconsultoria.com.br/{self.file.file_path}"

        _, file_extension = os.path.splitext(self.file.file_path)
        restricted_text = " (RESTRITO PARA INSCRITOS)" if self.file.restricted else ""
        file_name = StringService.sanitize(self.file.file_name)
        full_file_name = f"{file_name}{restricted_text}{file_extension}"
        full_file_path = os.path.join(files_folder_path, full_file_name)

        if self.can_skip_download(full_file_path):
            logging.debug(f"Skipping download of '{file_name}' as it already exists locally.")

            return

        logging.info(f"Downloading file '{file_name}'")
        HttpService(url=full_file_url).download(dest_file_path=full_file_path)

    @staticmethod
    def can_skip_download(full_file_path: str) -> bool:
        if not os.path.exists(full_file_path):
            return False

        file_handler = open(full_file_path, "rb")
        file_size = len(file_handler.read())
        file_handler.close()

        return file_size > 0
