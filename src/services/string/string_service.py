import json
import os
import re


class StringService:

    @staticmethod
    def print_currency(value: float) -> str:
        return 'R$ {:0,.2f}'.format(float(value)).replace('.', ';').replace(',', '.').replace(';', ',')

    @staticmethod
    def print_bool(value: bool) -> str:
        return 'SIM' if value else 'NÃO'

    @staticmethod
    def read_db_string(db_string_bytes: bytes, encoding: str = "") -> str:
        if encoding == "":
            encoding = os.getenv('DB_ENCODING', 'utf-8')

        if db_string_bytes is None:
            return ''

        return db_string_bytes.decode(encoding=encoding)

    @staticmethod
    def sanitize_diacritics(input_string: str) -> str:
        mapping = {
            'À':'A', 'Á':'A', 'Â':'A', 'Ã':'A', 'Ä':'Ae',
            '&Auml;':'A', 'Å':'A', 'Ā':'A', 'Ą':'A', 'Ă':'A', 'Æ':'Ae',
            'Ç':'C', 'Ć':'C', 'Č':'C', 'Ĉ':'C', 'Ċ':'C', 'Ď':'D', 'Đ':'D',
            'Ð':'D', 'È':'E', 'É':'E', 'Ê':'E', 'Ë':'E', 'Ē':'E',
            'Ę':'E', 'Ě':'E', 'Ĕ':'E', 'Ė':'E', 'Ĝ':'G', 'Ğ':'G',
            'Ġ':'G', 'Ģ':'G', 'Ĥ':'H', 'Ħ':'H', 'Ì':'I', 'Í':'I',
            'Î':'I', 'Ï':'I', 'Ī':'I', 'Ĩ':'I', 'Ĭ':'I', 'Į':'I',
            'İ':'I', 'Ĳ':'IJ', 'Ĵ':'J', 'Ķ':'K', 'Ł':'L', 'Ľ':'L',
            'Ĺ':'L', 'Ļ':'L', 'Ŀ':'L', 'Ñ':'N', 'Ń':'N', 'Ň':'N',
            'Ņ':'N', 'Ŋ':'N', 'Ò':'O', 'Ó':'O', 'Ô':'O', 'Õ':'O',
            'Ö':'Oe', '&Ouml;':'Oe', 'Ø':'O', 'Ō':'O', 'Ő':'O', 'Ŏ':'O',
            'Œ':'OE', 'Ŕ':'R', 'Ř':'R', 'Ŗ':'R', 'Ś':'S', 'Š':'S',
            'Ş':'S', 'Ŝ':'S', 'Ș':'S', 'Ť':'T', 'Ţ':'T', 'Ŧ':'T',
            'Ț':'T', 'Ù':'U', 'Ú':'U', 'Û':'U', 'Ü':'Ue', 'Ū':'U',
            '&Uuml;':'Ue', 'Ů':'U', 'Ű':'U', 'Ŭ':'U', 'Ũ':'U', 'Ų':'U',
            'Ŵ':'W', 'Ý':'Y', 'Ŷ':'Y', 'Ÿ':'Y', 'Ź':'Z', 'Ž':'Z',
            'Ż':'Z', 'Þ':'T', 'à':'a', 'á':'a', 'â':'a', 'ã':'a',
            'ä':'ae', '&auml;':'ae', 'å':'a', 'ā':'a', 'ą':'a', 'ă':'a',
            'æ':'ae', 'ç':'c', 'ć':'c', 'č':'c', 'ĉ':'c', 'ċ':'c',
            'ď':'d', 'đ':'d', 'ð':'d', 'è':'e', 'é':'e', 'ê':'e',
            'ë':'e', 'ē':'e', 'ę':'e', 'ě':'e', 'ĕ':'e', 'ė':'e',
            'ƒ':'f', 'ĝ':'g', 'ğ':'g', 'ġ':'g', 'ģ':'g', 'ĥ':'h',
            'ħ':'h', 'ì':'i', 'í':'i', 'î':'i', 'ï':'i', 'ī':'i',
            'ĩ':'i', 'ĭ':'i', 'į':'i', 'ı':'i', 'ĳ':'ij', 'ĵ':'j',
            'ķ':'k', 'ĸ':'k', 'ł':'l', 'ľ':'l', 'ĺ':'l', 'ļ':'l',
            'ŀ':'l', 'ñ':'n', 'ń':'n', 'ň':'n', 'ņ':'n', 'ŉ':'n',
            'ŋ':'n', 'ò':'o', 'ó':'o', 'ô':'o', 'õ':'o', 'ö':'oe',
            '&ouml;':'oe', 'ø':'o', 'ō':'o', 'ő':'o', 'ŏ':'o', 'œ':'oe',
            'ŕ':'r', 'ř':'r', 'ŗ':'r', 'š':'s', 'ù':'u', 'ú':'u',
            'û':'u', 'ü':'ue', 'ū':'u', '&uuml;':'ue', 'ů':'u', 'ű':'u',
            'ŭ':'u', 'ũ':'u', 'ų':'u', 'ŵ':'w', 'ý':'y', 'ÿ':'y',
            'ŷ':'y', 'ž':'z', 'ż':'z', 'ź':'z', 'þ':'t', 'ß':'ss',
            'ſ':'ss', 'ый':'iy', 'А':'A', 'Б':'B', 'В':'V', 'Г':'G',
            'Д':'D', 'Е':'E', 'Ё':'YO', 'Ж':'ZH', 'З':'Z', 'И':'I',
            'Й':'Y', 'К':'K', 'Л':'L', 'М':'M', 'Н':'N', 'О':'O',
            'П':'P', 'Р':'R', 'С':'S', 'Т':'T', 'У':'U', 'Ф':'F',
            'Х':'H', 'Ц':'C', 'Ч':'CH', 'Ш':'SH', 'Щ':'SCH', 'Ъ':'',
            'Ы':'Y', 'Ь':'', 'Э':'E', 'Ю':'YU', 'Я':'YA', 'а':'a',
            'б':'b', 'в':'v', 'г':'g', 'д':'d', 'е':'e', 'ё':'yo',
            'ж':'zh', 'з':'z', 'и':'i', 'й':'y', 'к':'k', 'л':'l',
            'м':'m', 'н':'n', 'о':'o', 'п':'p', 'р':'r', 'с':'s',
            'т':'t', 'у':'u', 'ф':'f', 'х':'h', 'ц':'c', 'ч':'ch',
            'ш':'sh', 'щ':'sch', 'ъ':'', 'ы':'y', 'ь':'', 'э':'e',
            'ю':'yu', 'я':'ya'
        }

        for key, value in mapping.items():
            input_string = input_string.replace(key, value)

        return input_string

    @staticmethod
    def sanitize_non_alphanumerical(input_string: str) -> str:
        return re.sub('[^A-Za-z0-9\-]', '', input_string)

    @staticmethod
    def sanitize_html_entities(input_string: str) -> str:
        return re.sub('/&[A-Za-z]+;/', '', input_string)

    @staticmethod
    def sanitize_path(input_string: str) -> str:
        input_string = input_string.replace("\\", "-")
        input_string = input_string.replace("/", "-")

        return input_string

    @staticmethod
    def sanitize_spaces(input_string: str) -> str:
        input_string = input_string.replace(" ", "-")
        input_string = re.sub('-+', '-', input_string)

        return input_string

    @staticmethod
    def sanitize(input_string: str) -> str:
        input_string = StringService.sanitize_diacritics(input_string)
        input_string = StringService.sanitize_html_entities(input_string)
        input_string = StringService.sanitize_path(input_string)
        input_string = StringService.sanitize_spaces(input_string)
        input_string = StringService.sanitize_non_alphanumerical(input_string)

        return input_string

    @staticmethod
    def export_dict_as_json_string(input_dict: dict) -> str:
        return json.dumps(
            input_dict,
            sort_keys=True,
            indent=4,
            separators=(',', ': '),
            ensure_ascii=False,
        )

    @staticmethod
    def return_only_numbers(input_string: str, default_value: int = 0) -> int:
        sanitized_input = re.sub('[^0-9]', '', input_string)

        return int(sanitized_input) if sanitized_input != '' else default_value
