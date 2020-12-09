import requests

URL = 'https://www.mobafire.com'


class Api:
    def __init__(self, cache):
        self.cache = cache

    @staticmethod
    def url(path):
        return URL + path

    def visit(self, path, params=None, cache_path=None):
        if cache_path:
            cache = self.cache
            if cache.exists(cache_path):
                content = cache.read(cache_path)
            else:
                response = requests.get(URL + path, params)
                content = response.text
                cache.write(cache_path, content)

            return content
        else:
            response = requests.get(URL + path, params)
            return response.text, response.status_code

    def search(self, champion):
        return self.visit(
            '/league-of-legends/browse',
            params={'champion': champion},
            cache_path=f'search/{champion}.html'
        )

    def fetch_guide(self, champion, link):
        return self.visit(link, cache_path=f'guides/{champion}.html')

    def fetch_champions(self):
        return self.visit('/league-of-legends/champions', cache_path='champions.html')
