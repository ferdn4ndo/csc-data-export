from models.vacancy.vacancy_model import VacancyModel
from services.database.event_database_service import EventDatabaseService


class VacancyCollectionModel:
    event_code: int = 0
    vacancies = []

    def __init__(self, event_code: int) -> None:
        self.event_code = event_code
        self.vacancies = []

    def sync(self):
        db_vacancies = EventDatabaseService.fetch_event_vacancies(self.event_code)
        self.parse_db_vacancies(db_vacancies)

    def parse_db_vacancies(self, db_vacancies):
        self.vacancies = []

        for db_vacancy in db_vacancies:
            vacancy = VacancyModel(db_vacancy)
            self.vacancies.append(vacancy)

    def serialize(self) -> dict:
        return {
            "vagas": [vacancy.serialize() for vacancy in self.vacancies]
        }

    @staticmethod
    def export_headers() -> list:
        return [
            "Cód. Vaga",
            "Cód. Evento",
            "Nome da Vaga",
            "Valor Inscrição",
            "Quantidade",
            "Cadastro Reserva",
            "Total Inscrições",
            "Total Inscrições Pagas"
        ]

    def export_rows(self) -> list:
        return [list(vacancy.serialize().values()) for vacancy in self.vacancies]
