import logging
from models.billet.billet_legacy_model import BilletLegacyModel
from models.billet.billet_model import BilletModel
from services.database.subscription_database_service import SubscriptionDatabaseService
from services.string.string_service import StringService


class BilletCollectionModel:
    subscription_code: int = 0

    def __init__(self, subscription_code: int) -> None:
        self.subscription_code = subscription_code
        self.billets = []

    def sync(self):
        self.billets = []

        db_billets = SubscriptionDatabaseService.fetch_subscription_billets(self.subscription_code)
        self.parse_db_billets(db_billets)

        db_billets_legacy = SubscriptionDatabaseService.fetch_subscription_billets_legacy(self.subscription_code)
        self.parse_db_billets(db_billets_legacy, is_legacy=True)

    def parse_db_billets(self, db_billets, is_legacy: bool = False):
        for db_billet in db_billets:
            billet = BilletLegacyModel(db_billet) if is_legacy else BilletModel(db_billet)
            self.billets.append(billet)

    def serialize(self) -> dict:
        return {
            "boletos": [billet.serialize() for billet in self.billets]
        }

    @staticmethod
    def export_headers() -> list:
        return [
            "Cód. Boleto",
            "Cód. Insc",
            "Situação",
            "Valor",
            "Descrição",
            "Data Geracao",
            "Data Atualizacao",
            "Data Vencimento",
            "Linha Digitavel",
            "Linha Digitavel Formatada",
            "Token",
            "URL",
            "Cód. Status",
            "Desc. Status",
            "Gateway de Geração",
        ]

    def export_rows(self) -> list:
        lines = []

        for billet in self.billets:
            if isinstance(billet, BilletModel):
                lines.append(list(billet.serialize().values()))
            elif isinstance(billet, BilletLegacyModel):
                lines.append(self.export_legacy_billet_row(billet=billet))
            else:
                logging.error(f"Unknown billet type: {billet.__class__}")

        return lines

    @staticmethod
    def export_legacy_billet_row(billet: BilletLegacyModel) -> list:
        return [
            billet.code,
            billet.subscription_code,
            str(billet.status_text),
            StringService.print_currency(billet.paid_value),
            "Boleto gerado pelo sistema",
            str(billet.generated_at),
            str(billet.paid_at),
            str(billet.due_at),
            billet.numeric_line,
            "",
            "",
            "",
            billet.status_code,
            "",
            "BRADESCO_ANTIGO",
        ]
