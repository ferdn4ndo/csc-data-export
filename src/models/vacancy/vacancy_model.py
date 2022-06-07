from services.database.vacancy_database_service import VacancyDatabaseService
from services.string.string_service import StringService


class VacancyModel:
    vacancy_code: int = 0
    event_code: int = 0
    name: str = ""
    cost: float = 0.0
    quantity: int = 0
    is_reserved: bool = False

    def __init__(self, db_dict) -> None:
        self.parse_from_db_dict(db_dict)

    def parse_from_db_dict(self, db_dict):
        self.vacancy_code = int(db_dict["CodVaga"])
        self.event_code = int(db_dict["CodEvento"])
        self.name = StringService.read_db_string(db_dict["NomeVaga"])
        self.cost = self.parse_db_price(db_dict["PrecoVaga"])
        self.quantity, self.is_reserved = self.parse_db_quantity(db_dict["QtdVagas"])

    def serialize(self) -> dict:
        return {
            "cod_vaga": self.vacancy_code,
            "cod_evento": self.event_code,
            "nome": self.name,
            "valor_inscricao": StringService.print_currency(self.cost),
            "quantidade_vagas": self.quantity,
            "cadastro_reserva": StringService.print_bool(self.is_reserved),
            "total_inscricoes": VacancyDatabaseService.fetch_vacancy_total_subscriptions(
                vacancy_code=self.vacancy_code,
                event_code=self.event_code
            ),
            "total_inscricoes_pagas": VacancyDatabaseService.fetch_vacancy_total_paid_subscriptions(
                vacancy_code=self.vacancy_code,
                event_code=self.event_code
            ),
        }

    @staticmethod
    def parse_db_quantity(db_quantity: bytes) -> tuple:
        quantity_text = StringService.read_db_string(db_string_bytes=db_quantity)
        sanitized_quantity = StringService.return_only_numbers(input_string=quantity_text)
        is_reserved = sanitized_quantity == 0 or " + " in quantity_text

        return sanitized_quantity, is_reserved

    @staticmethod
    def parse_db_price(db_price: bytes) -> float:
        db_price_float = float(db_price) if str(db_price) != "" else 0.0

        return db_price_float if db_price_float < 100 else db_price_float / 100
