from decouple import config
import requests
import getpass
import sys
from pastebin.utils import get_file_type_from_extension


class PasteBin:

    def __init__(self):
        self.API_DEV_KEY = config('API_DEV_KEY')
        self.PASTE_API_URL = config('PASTE_API_URL')
        self.LOGIN_API_URL = config('LOGIN_API_URL')
        self.API_USER_KEY = config('API_USER_KEY', default=None)

        self._file_name, self._paste_name = self._get_file_name()
        self._paste()

    @staticmethod
    def _get_lines(file, start, end):
        _code_snippet = ""
        _generate_code = (x for i, x in enumerate(file) if i in range(start, end))
        for _line in _generate_code:
            _code_snippet += _line

        return _code_snippet

    def _read_file(self, _file_name):
        read_only_code_snippet = input("Enter 'f' for reading full file: ")

        if read_only_code_snippet.lower() == 'f':
            with open(_file_name, 'r') as f:
                _code = f.read()
            return _code
        else:
            start_line = int(input("Start line: "))
            end_line = int(input("End line: "))

            with open(_file_name, 'r') as f:
                _code = self._get_lines(f, start_line, end_line)
                return _code

    @staticmethod
    def _get_file_name():
        _file_name = input("Full file name to paste(with *.ext): ")
        _paste_name = input("Paste name: ")
        return _file_name, _paste_name

    def _get_api_user_key(self):
        _user_name = input("Pastebin username: ")
        _password = getpass.getpass("Pastebin password: ", stream=sys.stderr)

        login_data = {
            'api_dev_key': self.API_DEV_KEY,
            'api_user_name': _user_name,
            'api_user_password': _password
        }

        response = requests.post(self.LOGIN_API_URL, data=login_data)

        if response is not None:
            with open('.env', 'a') as f_env:
                f_env.write(f"\nAPI_USER_KEY={response.text}")
            return response.text
        else:
            return ""

    def _paste(self):
        _code_snippet = self._read_file(self._file_name)
        _, _extension = self._file_name.split('.')
        _api_user_key = self.API_USER_KEY if self.API_USER_KEY is not None else self._get_api_user_key()

        data = {
                'api_dev_key': self.API_DEV_KEY,
                'api_user_key': _api_user_key,
                'api_option': 'paste',
                'api_paste_name': self._paste_name,
                'api_paste_code': _code_snippet,
                'api_paste_format': get_file_type_from_extension(_extension)
            }

        res = requests.post(url=self.PASTE_API_URL, data=data)
        print(res.text)

