import logging

from models.vacancy.vacancy_collection_model import VacancyCollectionModel
from services.database.event_database_service import EventDatabaseService
from services.date.date_service import DateService
from services.string.string_service import StringService


class EventTypeEnum:
    EVENT_TYPE_PUBLIC_TENDER = "EVENT_TYPE_PUBLIC_TENDER"
    EVENT_TYPE_SELECTION_PROCESS = "EVENT_TYPE_SELECTION_PROCESS"

    value = "UNKNOWN"

    def __init__(self, db_value) -> None:
        self.value = self.parse_from_db_value(db_value)

    def parse_from_db_value(self, db_value: int) -> str:
        if db_value == 0:
            return self.EVENT_TYPE_SELECTION_PROCESS
        elif db_value == 1:
            return self.EVENT_TYPE_PUBLIC_TENDER
        else:
            return "UNKNOWN"

    def to_string(self) -> str:
        if self.value == self.EVENT_TYPE_PUBLIC_TENDER:
            return "CONCURSO_PUBLICO"
        elif self.value == self.EVENT_TYPE_SELECTION_PROCESS:
            return "PROCESSO_SELETIVO"
        else:
            return "DESCONHECIDO"

    def __str__(self):
        return self.to_string()


class EventModel:
    event_code: int = 0
    type: EventTypeEnum
    name: str = ""
    generate_billet: bool = False
    payment_info: str = ""
    opening_date: DateService
    subscription_end_date: DateService
    exam_date: DateService
    description: str = ""

    def __init__(self, db_dict) -> None:
        self.parse_from_db_dict(db_dict)

    def parse_from_db_dict(self, db_dict):
        self.event_code = int(db_dict["CodEvento"])
        self.type = EventTypeEnum(int(db_dict["TipoEvento"]))
        self.name = StringService.read_db_string(db_dict["NomeEvento"])
        self.generate_billet = int(db_dict["GeraBoleto"]) == 1
        self.payment_info = StringService.read_db_string(db_dict["InstrucoesPgto"])
        self.opening_date = DateService(db_dict["DataAbertura"])
        self.subscription_end_date = DateService(db_dict["DataFimInsc"])
        self.exam_date = DateService(db_dict["DataProva"])
        self.description = StringService.read_db_string(db_dict["Descricao"])

    def serialize(self, expand_vacancies: bool = True) -> dict:
        if expand_vacancies:
            logging.info(f"Serializing event ID #{self.event_code} with relations...")

        base_dict = {
            "cod_evento": self.event_code,
            "tipo": str(self.type),
            "nome": self.name,
            "gera_boleto": StringService.print_bool(self.generate_billet),
            "instrucoes_pgto": self.payment_info,
            "data_abertura_inscricoes": str(self.opening_date),
            "data_final_inscricoes": str(self.subscription_end_date),
            "data_prova": str(self.exam_date),
            "descricao": self.description,
            "total_inscricoes": EventDatabaseService.fetch_event_total_subscriptions(event_code=self.event_code),
            "total_inscricoes_pagas": EventDatabaseService.fetch_event_total_paid_subscriptions(
                event_code=self.event_code
            ),
        }

        if not expand_vacancies:
            return base_dict

        vacancy_collection = VacancyCollectionModel(event_code=self.event_code)
        vacancy_collection.sync()

        return {**base_dict, **vacancy_collection.serialize()}
