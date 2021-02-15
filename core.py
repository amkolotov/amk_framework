import quopri


class Application:

    @staticmethod
    def decode_value(val: str) -> str:
        val_bytes = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = quopri.decodestring(val_bytes)
        return val_decode_str.decode('UTF-8')

    def parse_input_data(self, data: str) -> dict:
        result = {}
        if data:
            params = data.split('&')
            for item in params:
                key, value = item.split('=')
                value = self.decode_value(value)
                result[key] = value
        return result

    def parse_wsgi_input_data(self, data: bytes) -> dict:
        result = {}
        if data:
            data_str = data.decode(encoding='utf-8')
            result = self.parse_input_data(data_str)
        return result

    @staticmethod
    def get_wsgi_input_data(env: dict) -> bytes:
        content_length = env.get('CONTENT_LENGTH')
        content_length = int(content_length) if content_length else 0
        data = env['wsgi.input'].read(content_length) if content_length > 0 else b''
        return data

    def __init__(self, urlpatterns: dict, controllers: list):
        """
        :param urls: словарь url: view
        :param controllers: список front controllers
        """
        self.urls = urlpatterns
        self.controllers = controllers

    def __call__(self, environ, start_response):

        path = environ['PATH_INFO']
        if not path.endswith('/'):
            path += '/'

        method = environ['REQUEST_METHOD']
        data = self.get_wsgi_input_data(environ)
        data = self.parse_wsgi_input_data(data)

        query_string = environ['QUERY_STRING']
        request_params = self.parse_input_data(query_string)

        if path in self.urls:
            view = self.urls[path]
            request = {}
            request['method'] = method
            request['data'] = data
            request['request_params'] = request_params

            for controller in self.controllers:
                controller(request)
            code, text = view(request)
            start_response = (code, [('Content-type', 'text/html')])
            return [text.encode('utf-8')]
        else:
            start_response = ('404 NOT FOUND', [('Content-type', 'text/html')])
            return [b'Not found']
