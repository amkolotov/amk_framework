class Application:
    def __init__(self, urlpatterns: dict, controllers: list):
        """
        :param urls: словарь url: view
        :param controllers: список front controllers
        """
        self.urls = urlpatterns
        self.controllers = controllers

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        if path[-1] != '/':
            path += '/'
        if path in self.urls:
            view = self.urls[path]
            request = {}
            for controller in self.controllers:
                controller(request)
            code, text = view(request)
            start_response = (code, [('Content-type', 'text/html')])
            return [text.encode('utf-8')]
        else:
            start_response = ('404 NOT FOUND', [('Content-type', 'text/html')])
            return [b'Not found']
