from services.database.database_service import DatabaseService


class SubscriptionDatabaseService:

    @staticmethod
    def fetch_subscription_billets(subscription_code: int) -> list:
        query = f"SELECT * FROM tblBoletoNovo WHERE CodInsc = {subscription_code};"

        return DatabaseService().fetch_all_query_results(query)

    @staticmethod
    def fetch_subscription_billets_legacy(subscription_code: int) -> list:
        query = f"SELECT * FROM tblBoletos WHERE CodInsc = {subscription_code};"

        return DatabaseService().fetch_all_query_results(query)
