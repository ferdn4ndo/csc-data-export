import logging

from models.event.event_model import EventModel
from services.database.event_database_service import EventDatabaseService


class EventCollectionModel:
    events: list

    def __init__(self) -> None:
        self.events = []

    def sync(self):
        db_events = EventDatabaseService.fetch_events()
        self.events = [EventModel(db_event) for db_event in db_events]

    def serialize(self) -> dict:
        total_events = len(self.events)
        serialized_events = []

        for index, event in enumerate(self.events):
            logging.info(
                f"Serializing event ID #{event.event_code} ({index + 1} of {total_events})..."
            )
            serialized_events.append(event.serialize())

        return {"eventos": serialized_events}

    @staticmethod
    def export_headers() -> list:
        return [
            "Cód. Evento",
            "Tipo",
            "Nome",
            "Gera boleto?",
            "Instruções Pgto.",
            "Data Abertura Insc.",
            "Data Fim Insc.",
            "Data Prova",
            "Descrição",
            "Total Inscrições",
            "Total Inscrições Pagas"
        ]

    def export_rows(self) -> list:
        lines = []

        for event in self.events:
            serialized_event = event.serialize(expand_vacancies=False)
            lines.append(list(serialized_event.values()))

        return lines
