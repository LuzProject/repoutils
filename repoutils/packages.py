# module imports
from multiprocessing.pool import ThreadPool

class Package:
    def __init__(self, string: str = None, dictionary: str = None, repo_uri: str = None, thread_pool: ThreadPool = None):
        # repo uri
        self.repo_uri = repo_uri
        # define dictionary
        self.dict = {}
        if string:
            self.__parse_string(string)
        elif not dictionary:
            raise ValueError('No data provided.')
        
        # get objects prepared
        self.package: str = None
        self.name: str = None
        self.version: str = None
        self.filename: str = None
        self.size: str = None
        self.md5sum: str = None
        self.sha1: str = None
        self.sha256: str = None
        self.sha512: str = None
        self.section: str = None
        self.priority: str = None
        self.depends: str = None
        self.recommends: str = None
        self.suggests: str = None
        self.essential: bool = False
        self.pre_depends: str = None
        self.maintainer: str = None
        self.architecture: str = None
        self.description: str = None
        self.homepage: str = None
        self.bugs: str = None

        # t
        with (thread_pool or ThreadPool()) as pool:
            pool.map(self.__handle_key, self.dict.keys())

    
    def get_download_uri(self) -> str:
        if not self.repo_uri:
            raise ValueError('No repo URI provided.')
        return f'{self.repo_uri}/{self.filename}'


    def __handle_key(self, key: str) -> str:
        key_formatted = key.lower().replace(' ', '_').replace('-', '_')
        if key == 'Essential' and self.dict[key] == 'yes':
            self.dict[key_formatted] = True
        elif key_formatted in self.__dict__:
            self.__dict__[key_formatted] = self.dict[key]


    def __parse_string(self, string: str) -> dict:
        # parse string
        last = ''
        if not string or string == '':
            raise ValueError('Could not parse string.')
        else:
            for line in string.splitlines():
                if line.startswith("#"):
                    continue
                if len(line.split(": ", 1)) == 1:
                    self.dict[last] += line
                    continue
                elif len(line.split(": ", 1)) != 2:
                    continue
                key, value = line.split(": ", 1)
                last = key
                self.dict[key] = value
            return self.dict