import json
import time
from tqdm import tqdm

from vk_api import VkApi
from yd_api import YaUploader

# "Получаем токены из файла"
with open('my_token.txt', 'r') as file_object:
    token_vk = file_object.readline().strip()
    token_yd = file_object.readline().strip()

# "Указываем данные"
    vk_api_version = '5.131'
    user = None
    folder_name = 'Photos_from_VK'
    max_photos = 5

# "Получаем словарь с инфо по фото с профиля указанного пользователя (если есть право на просмотр профиля)
    # и создаем папку на Yandex Disc"
    source_url = VkApi(token_vk, vk_api_version)
    result = source_url.get_user_photo(max_photos, user)
    uploader = YaUploader(token_yd)
    uploader.create_folder(folder_name)

# Задаем имена файлам и загружаем их в созданную папку на Yandex Disc
    for c in range(len(result['links'])):
        file_path = folder_name + '/' + result['info'][c]["file_name"]
        link = result['links'][c]
        response = uploader.upload(link, file_path)

# Создаем json-файлы с информацией по каждому из загруженных файлов
        lst = [result['info'][c]]
        with open("log_{0}_({1}).json".format(c + 1, result['info'][c]["file_name"].split('.')[0]), "w") as f:
            json.dump(lst, f, ensure_ascii=False, indent=2)

# Выводим в консоль статус загрузки
        if response == 202:
            status = str('Uploading {0}'.format(result["info"][c]["file_name"]))
            for i in tqdm(range(1, 5), desc=status, colour='#2F4F4F', bar_format='{l_bar}{bar}|'):
                time.sleep(0.2)
        else:
            status = str('File {0} upload failed'.format(result["info"][c]["file_name"]))
            print(status)
