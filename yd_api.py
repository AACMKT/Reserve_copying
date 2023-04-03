import requests
import time


class YaUploader:
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token),
        }

    def create_folder(self, folder_name):
        """Создает папку на Yandex Disc. Выводит сообщение о результате работы"""

        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        path = folder_name
        fields = {
            'Resource': 'name,path,size'
        }
        request = {"path": path, "fields": fields}
        response = requests.put(upload_url, headers=self.headers, params=request)
        if response.status_code == 201:
            print(f'Folder {path} successfully created\n')
        elif response.status_code == 409:
            print('Folder already exists\n')
        else:
            print('Unexpected failure during folder creation occurred\n')
        time.sleep(0.33)

    def upload(self, link, file_path: str):
        """Загружает файлы по ссылкам в указанную директорию
         (путь к конечной директории предполагает указание имени самого сохраняемого файла)"""

        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        file_url = link
        request = {"url": file_url, "path": file_path}
        response = requests.post(upload_url, headers=self.headers, params=request)
        return response.status_code
