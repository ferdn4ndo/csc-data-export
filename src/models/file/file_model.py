from services.date.date_service import DateService
from services.string.string_service import StringService


class FileModel:
    code: int = 0
    event_code: int = 0
    restricted: bool = False
    file_name: str = ""
    total_downloads: int = 0
    file_path: str = ""
    uploaded_at: DateService


    def __init__(self, db_dict) -> None:
        self.parse_from_db_dict(db_dict)

    def parse_from_db_dict(self, db_dict):
        self.code = int(db_dict["CodArquivo"])
        self.event_code = int(db_dict["CodEvento"])
        self.restricted = int(db_dict["RestritoInsc"]) == 1
        self.file_name = StringService.read_db_string(db_dict["NomeArquivo"])
        self.total_downloads = int(db_dict["DownsArquivo"])
        self.file_path = StringService.read_db_string(db_dict["CaminhoArquivo"])
        self.uploaded_at = DateService(db_dict["DataEnvio"])

    def serialize(self) -> dict:
        return {
            "cod_arquivo": self.code,
            "cod_evento": self.event_code,
            "restrito_para_inscritos": "SIM" if self.restricted else "NÃO",
            "nome_arquivo": self.file_name,
            "total_downloads": self.total_downloads,
            "caminho_arquivo": self.file_path,
            "data_envio": str(self.uploaded_at),
        }
