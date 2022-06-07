from services.database.database_service import DatabaseService


class EventDatabaseService:

    @staticmethod
    def fetch_events() -> list:
        query = f"SELECT * FROM tblEventos;"

        return DatabaseService().fetch_all_query_results(query)

    @staticmethod
    def fetch_event_files(event_code: int) -> list:
        query = f"SELECT * FROM tblArquivos WHERE CodEvento = {event_code};"

        return DatabaseService().fetch_all_query_results(query)

    @staticmethod
    def fetch_event_subscriptions(event_code: int) -> list:
        query = f"SELECT * FROM tblInscricoes INNER JOIN tblVagas ON tblInscricoes.CodVaga = tblVagas.CodVaga WHERE tblInscricoes.CodEvento = {event_code};"

        return DatabaseService().fetch_all_query_results(query)

    @staticmethod
    def fetch_event_vacancies(event_code: int) -> list:
        query = f"SELECT * FROM tblVagas WHERE CodEvento = {event_code};"

        return DatabaseService().fetch_all_query_results(query)

    @staticmethod
    def fetch_event_total_subscriptions(event_code: int) -> int:
        query = f"SELECT COUNT(*) FROM tblInscricoes WHERE CodEvento = {event_code};"

        return int(DatabaseService().fetch_query_first_column(query))

    @staticmethod
    def fetch_event_total_paid_subscriptions(event_code: int) -> int:
        query = f"SELECT COUNT(*) FROM tblInscricoes WHERE CodEvento = {event_code} AND EstInsc = 2"

        return int(DatabaseService().fetch_query_first_column(query))
