import requests
from bs4 import BeautifulSoup
from concurrent import futures


class GetPage:
    default_files = ['pdf', 'txt', 'doc', 'cbr', 'epub']

    def __init__(self, url):
        protocol = 'https://'
        if protocol in url:
            self._request = requests.get(url)
            self._url = url
        else:
            url_c = protocol + url
            self._request = requests.get(url_c)
            self._url = url_c

        self._s = BeautifulSoup(self._request.content, 'html.parser', from_encoding="iso-8859-1")
        self._files = (tag.get('href') for tag in self._s.find_all('a'))

    def get_links(self, exten=default_files):
        """Pega os links de acordo com a extensão"""
        links = set()
        if type(exten) == str:
            for file_link in self._files:
                if exten in file_link:
                    links.add(file_link)
        else:
            for extension in exten:
                print(extension)
                for file_link in self._files:
                    if extension in file_link:
                        links.add(file_link)
        return links

    def _download_handler(self, link):
            complete_link = self._url + link
            r = requests.get(complete_link, stream=True)
            with open(f'downloads/{link}', 'wb') as f:
                for chunk in r.iter_content(1024):
                    if chunk:
                        f.write(chunk)

    def download(self, exten=default_files, threads=4):
        links = self.get_links(exten)
        with futures.ThreadPoolExecutor(threads) as exec_:
            exec_.map(self._download_handler, links)
