from services.date.date_service import DateService
from services.string.string_service import StringService


class BilletLegacyStatusEnum:
    BILLET_LEGACY_STATUS_OPEN = "BILLET_STATUS_OPEN"
    BILLET_LEGACY_STATUS_PAID = "BILLET_STATUS_PAID"

    value = "UNKNOWN"

    def __init__(self, db_value) -> None:
        self.value = self.parse_from_db_value(db_value)

    def parse_from_db_value(self, db_value: str) -> str:
        if db_value == "011" or db_value == "015" or db_value == "021":
            return self.BILLET_LEGACY_STATUS_PAID
        elif db_value == "014" or db_value == "010":
            return self.BILLET_LEGACY_STATUS_OPEN
        else:
            return "UNKNOWN"

    def to_string(self) -> str:
        if self.value == self.BILLET_LEGACY_STATUS_OPEN:
            return "EM_ABERTO"
        elif self.value == self.BILLET_LEGACY_STATUS_PAID:
            return "PAGO"
        else:
            return "DESCONHECIDO"

    def __str__(self):
        return self.to_string()

class BilletLegacyModel:
    code: int = 0
    subscription_code: int = 0
    numeric_line: str = ""
    generated_at: DateService
    due_at: DateService
    paid_at: DateService
    paid_value: float = 0.0
    status_code: str = ""
    status_text: BilletLegacyStatusEnum

    def __init__(self, db_dict) -> None:
        self.parse_from_db_dict(db_dict)

    def parse_from_db_dict(self, db_dict):
        self.code = int(db_dict["CodBoleto"])
        self.subscription_code = int(db_dict["CodInsc"])
        self.numeric_line = StringService.read_db_string(db_dict["NumBoleto"])
        self.generated_at = DateService(db_dict["DataEmitido"])
        self.due_at = DateService(db_dict["DataVencimento"])
        self.paid_at = DateService(db_dict["DataPago"])
        self.paid_value = (float(db_dict["ValorPago"]) / 100) if db_dict["ValorPago"] is not None else 0
        self.status_code = StringService.read_db_string(db_dict["Status"])
        self.status_text = BilletLegacyStatusEnum(self.status_code)

    def serialize(self) -> dict:
        return {
            "cod_boleto": self.code,
            "cod_insc": self.subscription_code,
            "linha_digitavel": self.numeric_line,
            "data_geracao": str(self.generated_at),
            "data_vencimento": str(self.due_at),
            "data_pagamento": str(self.paid_at),
            "valor_pago": StringService.print_currency(self.paid_value),
            "situacao_boleto": str(self.status_text),
            "cod_situacao_boleto": self.status_code,
            "gateway": "BRADESCO_ANTIGO",
        }
