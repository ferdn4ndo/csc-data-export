from models.file.file_model import FileModel
from services.database.event_database_service import EventDatabaseService


class FileCollectionModel:
    event_code: int = 0
    files = []

    def __init__(self, event_code: int) -> None:
        self.event_code = event_code
        self.files = []

    def sync(self):
        db_files = EventDatabaseService.fetch_event_files(event_code=self.event_code)
        self.files = [FileModel(db_file) for db_file in db_files]

    def serialize(self) -> dict:
        return {
            "arquivos": [file.serialize() for file in self.files]
        }

    @staticmethod
    def export_headers() -> list:
        return [
            "Cód. Arquivo",
            "Cód. Evento",
            "Restrito p/ Inscritos",
            "Nome",
            "Downloads",
            "Caminho",
            "Data de Envio",
        ]

    def export_rows(self) -> list:
        return [list(file.serialize().values()) for file in self.files]
