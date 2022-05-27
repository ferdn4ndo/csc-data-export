import logging

from models.event.event_collection_model import EventCollectionModel
from models.event.event_model import EventModel
from models.file.file_collection_model import FileCollectionModel
from models.subscription.subscription_collection_model import SubscriptionCollectionModel
from models.vacancy.vacancy_collection_model import VacancyCollectionModel
from services.event.event_file_service import EventFileService
from services.event.event_folder_service import EventFolderService
from services.string.string_service import StringService
from services.worksheet.worksheet_service import WorksheetService


class EventExportService:
    event: EventModel

    def __init__(self, event: EventModel) -> None:
        self.event = event

    def save_event_file(self, inner_path: str, content: str) -> None:
        folder_service = EventFolderService(event=self.event)
        folder_service.create_event_folder_if_not_exists()

        event_folder_path = folder_service.get_event_folder()

        json_file_path = f"{event_folder_path}/{inner_path}"
        with open(json_file_path, 'w') as f:
            f.write(content)

    def save_event_worksheet(self, inner_path: str, headers: list, rows: list, title: str) -> None:
        folder_service = EventFolderService(event=self.event)
        folder_service.create_event_folder_if_not_exists()

        event_folder_path = folder_service.get_event_folder()
        worksheet_file_path = f"{event_folder_path}/{inner_path}"

        logging.info(f"Exporting spreadsheet file '{inner_path}'...")
        worksheet = WorksheetService(headers=headers, rows=rows, title=title)
        worksheet.save(filepath=worksheet_file_path)

    def export_collection(self, collection, filename: str, title: str) -> None:
        collection.sync()

        self.save_event_file(
            f"{filename}.json",
            StringService.export_dict_as_json_string(collection.serialize())
        )

        self.save_event_worksheet(
            inner_path=f"{filename}.xlsx",
            headers=collection.export_headers(),
            rows=collection.export_rows(),
            title=title
        )

    def export_event_info(self) -> None:
        self.save_event_file(
            "informacoes_do_evento.json",
            StringService.export_dict_as_json_string(self.event.serialize())
        )

    def export_event_subscriptions(self) -> None:
        collection = SubscriptionCollectionModel(event_code=self.event.event_code)

        self.export_collection(
            collection=collection,
            filename="lista_de_inscricoes",
            title=f"Lista de inscritos no evento {self.event.name}"
        )

    def export_event_vacancies(self) -> None:
        collection = VacancyCollectionModel(event_code=self.event.event_code)

        self.export_collection(
            collection=collection,
            filename="lista_de_vagas",
            title=f"Lista de vagas do evento {self.event.name}"
        )

    def export_event_files(self) -> None:
        collection = FileCollectionModel(self.event.event_code)

        self.export_collection(
            collection=collection,
            filename="lista_de_arquivos",
            title=f"Lista de arquivos do evento {self.event.name}"
        )

        for file in collection.files:
            service = EventFileService(event=self.event, file=file)
            service.download()

    def export(self) -> None:
        self.export_event_info()
        self.export_event_vacancies()
        self.export_event_files()
        self.export_event_subscriptions()


def export_all_events():
    logging.info("=== STARTING FULL EXPORT ===")
    collection = EventCollectionModel()
    collection.sync()

    data_folder = EventFolderService.get_data_folder()

    worksheet_file_path = f"{data_folder}/eventos.xlsx"
    logging.info(f"Exporting events list spreadsheet to '{worksheet_file_path}'...")
    worksheet = WorksheetService(
        headers=collection.export_headers(),
        rows=collection.export_rows(),
        title="Eventos cadastrados na CSC Consultoria"
    )
    worksheet.save(filepath=worksheet_file_path)

    json_file_path = f"{data_folder}/eventos.json"
    logging.info(f"Exporting events list json to '{json_file_path}'...")
    with open(json_file_path, 'w') as f:
        f.write(StringService.export_dict_as_json_string(collection.serialize()))

    total_events = len(collection.events)
    for index, event in enumerate(collection.events):
        logging.info(f"Exporting event #{event.event_code} ({index + 1} of {total_events}): {event.name}")
        service = EventExportService(event=event)
        service.export()

    logging.info("=== FINISHED FULL EXPORT ===")
