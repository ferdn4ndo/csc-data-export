import logging
import sys

from services.event.event_export_service import export_all_events

log_formatter = logging.Formatter("%(asctime)s [%(filename)s:%(lineno)d] [%(levelname)s] %(message)s")
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_formatter)
root_logger.addHandler(console_handler)

file_handler = logging.FileHandler("/code/data/output.log", mode="w")
file_handler.setFormatter(log_formatter)
root_logger.addHandler(file_handler)


if __name__ == "__main__":
    export_all_events()
