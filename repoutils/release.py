# module imports
from requests import get
from multiprocessing.pool import ThreadPool
from warnings import filterwarnings

# local imports
from .packages import Package

filterwarnings('ignore')


class Release:
    def __init__(self, url: str = None, suite: str = None, component: str = None, thread_pool: ThreadPool = None):
        # pool
        self.pool = thread_pool if thread_pool else ThreadPool()
        # dist
        self.suite = suite
        self.component = component
        # url
        self.url = url.split('Release')[0]
        self.furl = url
        # define dictionary
        self.dict = {}
        self.__get_url()
        
        # parse dict
        self.architectures: str = self.dict.get('Architectures')
        self.codename: str = self.dict.get('Codename')
        self.components: str = self.dict.get('Components')
        self.description: str = self.dict.get('Description')
        self.label: str = self.dict.get('Label')
        self.origin: str = self.dict.get('Origin')
        self.suite: str = self.dict.get('Suite')
        self.version: str = self.dict.get('Version')
        self.date: str = self.dict.get('Date')

        # packages
        self.packages: list[Package] = []
        self.__get_packages()

    
    def __parse_package(self, string: str):
        self.packages.append(Package(string, repo_uri=self.url))


    def __get_packages(self):
        packages_str = ''
        # attempt to find packages file
        try:
            if self.component is not None:
                with get(self.furl + f'/{self.component}/binary-{self.architectures.split(" ")[0]}/Packages', verify=False) as req:
                    if req.ok:
                        packages_str = req.text
            else:
                with get(self.furl + '/Packages', verify=False) as req:
                    if req.ok:
                        packages_str = req.text
            # error if failed
            if packages_str == '':
                raise ValueError('Could not get packages file.')
        except:
            raise ValueError('Could not get packages file.')

        # parse packages
        packages = list(filter(lambda x: x != '', packages_str.split('\n\n')))
        
        self.pool.map(self.__parse_package, packages)
        
    
    def __get_url(self):
        # get data from url
        url = self.url
        try:
            if self.suite is not None: 
                self.furl += f'/dists/{self.suite}'
                url += f'/dists/{self.suite}'
            url += '/Release'
            with get(url, verify=False) as req:
                self.__parse_string(req.text)
        except:
            raise ValueError('Could not get url. Maybe it uses dists?')

    def __parse_string(self, string: str) -> dict:
        # parse string
        if not string or string == '':
            raise ValueError('Could not parse string.')
        else:
            for line in string.splitlines():
                if line.startswith("#"):
                    continue
                if len(line.split(": ", 1)) != 2:
                    continue
                key, value = line.split(": ", 1)
                self.dict[key] = value
            return self.dict