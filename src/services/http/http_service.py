import requests

class HttpMethods:
    HTTP_METHOD_GET = "get"
    HTTP_METHOD_POST = "post"
    HTTP_METHOD_PUT = "put"
    HTTP_METHOD_PATCH = "patch"
    HTTP_METHOD_DELETE = "delete"
    HTTP_METHOD_HEAD = "head"
    HTTP_METHOD_OPTIONS = "options"


class HttpService:
    url: str = ""
    method: str = HttpMethods.HTTP_METHOD_GET

    def __init__(self, url: str, method: str = HttpMethods.HTTP_METHOD_GET):
        self.url = url
        self.method = method

    @staticmethod
    def get_request_headers() -> dict:
        return {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }

    def download(self, dest_file_path: str) -> None:
        with open(dest_file_path, "wb") as outputFile:
            method_caller = getattr(requests, self.method)
            content = method_caller(url=self.url, headers=self.get_request_headers(), stream=True).content
            outputFile.write(content)
