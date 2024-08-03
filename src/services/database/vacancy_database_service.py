from services.database.database_service import DatabaseService


class VacancyDatabaseService:

    @staticmethod
    def fetch_vacancy(vacancy_code: int) -> dict:
        query = f"SELECT * FROM tblVagas WHERE CodVaga = {vacancy_code};"

        return DatabaseService().fetch_one_query_row(query)

    @staticmethod
    def fetch_vacancy_total_subscriptions(event_code: int, vacancy_code: int) -> int:
        query = f"SELECT COUNT(*) FROM tblInscricoes WHERE CodVaga = {vacancy_code} AND CodEvento = {event_code}"

        return int(DatabaseService().fetch_query_first_column(query))

    @staticmethod
    def fetch_vacancy_total_paid_subscriptions(event_code: int, vacancy_code: int) -> int:
        query = f"SELECT COUNT(*) FROM tblInscricoes WHERE CodVaga = {vacancy_code} AND CodEvento = {event_code} AND EstInsc = 2"

        return int(DatabaseService().fetch_query_first_column(query))
