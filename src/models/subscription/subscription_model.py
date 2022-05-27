import logging

from models.billet.billet_collection_model import BilletCollectionModel
from services.date.date_service import DateService
from services.string.string_service import StringService


class SubscriptionStatusEnum:
    SUBSCRIPTION_STARTED = "SUBSCRIPTION_STARTED"
    SUBSCRIPTION_WAITING_PAYMENT = "SUBSCRIPTION_WAITING_PAYMENT"
    SUBSCRIPTION_PAYMENT_CONFIRMED = "SUBSCRIPTION_PAYMENT_CONFIRMED"

    value = "UNKNOWN"

    def __init__(self, db_value: int) -> None:
        self.value = self.parse_from_db_value(db_value)

    def parse_from_db_value(self, db_value: int) -> str:
        if db_value == 0:
            return self.SUBSCRIPTION_STARTED
        elif db_value == 1:
            return self.SUBSCRIPTION_WAITING_PAYMENT
        elif db_value == 2:
            return self.SUBSCRIPTION_PAYMENT_CONFIRMED
        else:
            return "UNKNOWN"

    def to_string(self) -> str:
        if self.value == self.SUBSCRIPTION_STARTED:
            return "INCOMPLETA"
        elif self.value == self.SUBSCRIPTION_WAITING_PAYMENT:
            return "AGUARDANDO_PAGAMENTO"
        elif self.value == self.SUBSCRIPTION_PAYMENT_CONFIRMED:
            return "PAGAMENTO_CONFIRMADO"
        else:
            return "DESCONHECIDO"

    def __str__(self):
        return self.to_string()


class SubscriptionModel:
    subscription_code: int = 0
    event_code: int = 0
    vacancy_code: int = 0
    vacancy_name: str = ""
    name: str = ""
    email: str = ""
    rg: str = ""
    cpf: int = 0
    birth_date: DateService
    address: str = ""
    number: int = 0
    complement: str = ""
    city: str = ""
    state: str = ""
    zip_code: int = 0
    phone: int = 0
    has_special_needs: bool = False
    special_need_type: str = ""
    special_need_code: str = ""
    doctor_name: str = ""
    special_exam_type: str = ""
    main_billet_code: int = 0
    subscription_status: SubscriptionStatusEnum

    def __init__(self, db_dict) -> None:
        self.parse_from_db_dict(db_dict)

    def parse_from_db_dict(self, db_row):
        self.subscription_code = int(db_row["CodInsc"])
        self.event_code = int(db_row["CodEvento"])
        self.vacancy_code = int(db_row["CodVaga"])
        self.vacancy_name = StringService.read_db_string(db_row["NomeVaga"])
        self.name = StringService.read_db_string(db_row["Nome"])
        self.email = StringService.read_db_string(db_row["Email"])
        self.rg = StringService.read_db_string(db_row["RG"])
        self.cpf = int(db_row["CPF"])
        self.birth_date = DateService(db_row["DataNasc"])
        self.address = StringService.read_db_string(db_row["Endereco"])
        self.number = int(db_row["Numero"]) if db_row["Numero"] is not None else 0
        self.complement = StringService.read_db_string(db_row["Complemento"])
        self.city = StringService.read_db_string(db_row["Cidade"])
        self.state = StringService.read_db_string(db_row["UF"])
        self.zip_code = int(db_row["CEP"])
        self.phone = int(db_row["Telefone"]) if db_row["Telefone"] is not None else 0
        self.has_special_needs = int(db_row["Necessidades"]) == 1
        self.special_need_type = StringService.read_db_string(db_row["TipoDeficiencia"])
        self.special_need_code = StringService.read_db_string(db_row["Cid"])
        self.doctor_name = StringService.read_db_string(db_row["NomeMedico"])
        self.special_exam_type = StringService.read_db_string(db_row["TipoProva"])
        self.main_billet_code = int(db_row["CodBoleto"]) if db_row["CodBoleto"] is not None else 0
        self.subscription_status = SubscriptionStatusEnum(int(db_row["EstInsc"]))

    def serialize(self, expand_billets: bool = True) -> dict:
        base_dict = {
            "cod_inscricao": self.subscription_code,
            "cod_evento": self.event_code,
            "cod_vaga": self.vacancy_code,
            "nome_vaga": self.vacancy_name,
            "nome": self.name,
            "email": self.email,
            "rg": self.rg,
            "cpf": self.cpf,
            "data_nascimento": str(self.birth_date),
            "endereco": self.address,
            "numero": self.number,
            "complemento": self.complement,
            "cidade": self.city,
            "estado": self.state,
            "cep": self.zip_code,
            "telefone": self.phone,
            "possui_necessidades_especiais": self.has_special_needs,
            "tipo_deficiencia": self.special_need_type,
            "cid": self.special_need_code,
            "nome_medico": self.doctor_name,
            "tipo_prova": self.special_exam_type,
            "cod_boleto_principal": self.main_billet_code,
            "situacao": str(self.subscription_status),
        }

        if not expand_billets:
            return base_dict

        billet_collection = BilletCollectionModel(subscription_code=self.subscription_code)
        billet_collection.sync()

        return {**base_dict, **billet_collection.serialize()}
