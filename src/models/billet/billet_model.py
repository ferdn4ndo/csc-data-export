from services.date.date_time_service import DateTimeService
from services.string.string_service import StringService


class BilletStatusEnum:
    BILLET_STATUS_ERROR = "BILLET_STATUS_ERROR"
    BILLET_STATUS_OPEN = "BILLET_STATUS_OPEN"
    BILLET_STATUS_PAID = "BILLET_STATUS_PAID"

    value = "UNKNOWN"

    def __init__(self, db_value) -> None:
        self.value = self.parse_from_db_value(db_value)

    def parse_from_db_value(self, db_value: int) -> str:
        if db_value == -1:
            return self.BILLET_STATUS_ERROR
        elif db_value == 0:
            return self.BILLET_STATUS_OPEN
        elif db_value == 1:
            return self.BILLET_STATUS_PAID
        else:
            return "UNKNOWN"

    def to_string(self) -> str:
        if self.value == self.BILLET_STATUS_ERROR:
            return "COM_ERRO"
        elif self.value == self.BILLET_STATUS_OPEN:
            return "EM_ABERTO"
        elif self.value == self.BILLET_STATUS_PAID:
            return "PAGO"
        else:
            return "DESCONHECIDO"

    def __str__(self):
        return self.to_string()

class BilletModel:
    code: int = 0
    subscription_code: int = 0
    status: BilletStatusEnum
    value: float = 0.0
    description: str = ""
    generated_at: DateTimeService
    updated_at: DateTimeService
    due_at: DateTimeService
    numeric_line: str = ""
    formatted_numeric_line: str = ""
    token: str = ""
    access_url: str = ""
    bank_status_code: int = 0
    bank_status_description: str = ""

    def __init__(self, db_dict) -> None:
        self.parse_from_db_dict(db_dict)

    def parse_from_db_dict(self, db_dict):
        self.code = int(db_dict["CodBoleto"])
        self.subscription_code = int(db_dict["CodInsc"])
        self.status = BilletStatusEnum(int(db_dict["SituacaoBoleto"]))
        self.value = (float(db_dict["ValorBoleto"]) / 100) if db_dict["ValorBoleto"] is not None else 0
        self.description = StringService.read_db_string(db_dict["DescricaoBoleto"])
        self.generated_at = DateTimeService(db_dict["DataGeracao"])
        self.updated_at = DateTimeService(db_dict["DataAtualizacao"])
        self.due_at = DateTimeService(db_dict["DataVencimento"])
        self.numeric_line = StringService.read_db_string(db_dict["LinhaDigitavel"])
        self.formatted_numeric_line = StringService.read_db_string(db_dict["LinhaDigFormatada"])
        self.token = StringService.read_db_string(db_dict["Token"])
        self.access_url = StringService.read_db_string(db_dict["URLAcesso"])
        self.bank_status_code = int(db_dict["CodStatus"]) if db_dict["CodStatus"] is not None else 0
        self.bank_status_description = StringService.read_db_string(db_dict["DescStatus"])

    def serialize(self) -> dict:
        return {
            "cod_boleto": self.code,
            "cod_insc": self.subscription_code,
            "situacao_boleto": str(self.status),
            "valor_boleto": StringService.print_currency(self.value),
            "descricao_boleto": self.description,
            "data_geracao": str(self.generated_at),
            "data_atualizacao": str(self.updated_at),
            "data_vencimento": str(self.due_at),
            "linha_digitavel": self.numeric_line,
            "linha_digitavel_formatada": self.formatted_numeric_line,
            "token": self.token,
            "url_acesso": self.access_url,
            "cod_status_geracao": self.bank_status_code,
            "texto_status_geracao": self.bank_status_description,
            "gateway": "BRADESCO_NOVO",
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
        return [*self.serialize().values()]
