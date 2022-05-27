from datetime import datetime, date

from services.string.string_service import StringService


class DateTimeService:
    date_object: date

    def __init__(self, db_value: bytes) -> None:
        self.date_object = self.parse_from_db_value(StringService.read_db_string(db_value))

    @staticmethod
    def parse_from_db_value(db_date: str) -> [date]:
        if db_date == "" or db_date == "0000-00-00 00:00:00":
            return None

        return datetime.strptime(db_date, '%Y-%m-%d %H:%M:%S')

    def to_string(self) -> str:
        if self.date_object is None:
            return ""

        return self.date_object.strftime('%d/%m/%Y %H:%M:%S')

    def __str__(self):
        return self.to_string()
