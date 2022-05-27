import logging

from models.subscription.subscription_model import SubscriptionModel
from services.database.event_database_service import EventDatabaseService


class SubscriptionCollectionModel:
    event_code: int = 0
    subscriptions = []

    def __init__(self, event_code: int) -> None:
        self.event_code = event_code
        self.subscriptions = []

    def sync(self):
        db_subscriptions = EventDatabaseService.fetch_event_subscriptions(self.event_code)
        self.subscriptions = [SubscriptionModel(db_subscription) for db_subscription in db_subscriptions]

    def serialize(self) -> dict:
        total_subscriptions = len(self.subscriptions)
        serialized_subscriptions = []

        for index, subscription in enumerate(self.subscriptions):
            logging.info(
                f"Serializing subscription ID #{subscription.subscription_code} ({index+1} of {total_subscriptions})..."
            )
            serialized_subscriptions.append(subscription.serialize())

        return {"inscricoes": serialized_subscriptions}

    @staticmethod
    def export_headers() -> list:
        return [
            "Cód. Inscrição",
            "Cód. Evento",
            "Cód. Vaga",
            "Vaga",
            "Nome",
            "E-mail",
            "RG",
            "CPF",
            "Data Nasc.",
            "Endereço",
            "Número",
            "Complemento",
            "Cidade",
            "UF",
            "CEP",
            "Telefone",
            "PNE",
            "Tipo de Deficiência",
            "CID",
            "Nome do Médico",
            "Tipo de Prova Especial",
            "Cód. Boleto Principal",
            "Situação",
        ]

    def export_rows(self) -> list:
        lines = []

        for subscription in self.subscriptions:
            serialized_subscription = subscription.serialize(expand_billets=False)

            lines.append(list(serialized_subscription.values()))

        return lines
