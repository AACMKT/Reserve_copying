import requests
from pprint import pprint
from datetime import date


class VkApi:
    URL = 'https://api.vk.com/method/'

    def __init__(self, token, version):
        self.params = {
            'access_token': token,
            'v': version,
        }

    def get_user_photo(self, max_photos, user_id=None):
        """Получает список ссылок на фото из профиля пользователя, а также данные о фото.
        Функция возвращает словарь с max доступными размерами фото
        и сгенерированным именем фото: (кол-во лайков)_(дата загрузки фото на страницу)"""

        album_params = {
            'album_id': 'profile',
            'extended': 1,
            'owner_id': user_id,
            'photo_sizes': 1,
            'count': max_photos,
        }
        info = []
        href_ = []
        link = None
        description = {}

        res = requests.get(self.URL + 'photos.get', params={**self.params, **album_params}).json()
        for i in res['response']['items']:
            size = {}
            scale = {'s': 0, 'm': 1, 'x': 2, 'o': 3, 'p': 4, 'q': 5, 'r': 6, 'y': 7, 'z': 8, 'w': 9}
            v = {}
            name = None

            for s in i['sizes']:
                size = {**size, **{s['type']: scale[s['type']]}}
                max_size = max(size, key=size.get)
                if max_size in s['type']:
                    name = '{0}_{1}.jpg'.format(str(i['likes']['count']),
                                                str(date.fromtimestamp(i['date'])).replace('-', '_'))
                    link = s['url']

                v = {"file_name": name, 'size': max_size}

            info.append(v)
            href_.append(link)
            description['info'] = info
            description['links'] = href_
        return description

    def get_user(self, user_id):
        """Предоставляет данные о пользователе VK по его id.
        Если id не указан, возвращает данные о владельце токена"""

        usr_params = {
            'user_ids': user_id
        }
        res = requests.get(self.URL + 'users.get', params={**self.params, **usr_params})
        return res.json()

    def get_friends(self, user_id):
        """Предоставляет список с данными о друзьях пользователя VK по его id (id, Имя, Фамилия).
        Если id не указан, возвращает данные о владельце токена"""

        fr_params = {
            'user_ids': user_id,
            'fields': 'first_name, last_name',
        }
        res = requests.get(self.URL + 'friends.get', params={**self.params, **fr_params}).json()
        info = []
        for i in res['response']['items']:
            person = {'first_name': i['first_name'], 'last_name': i['last_name'], 'id': i['id']}
            info.append(person)
        pprint(info)


if __name__ == '__main__':
    with open('my_token.txt', 'r') as file_object:
        token_vk = file_object.readline().strip()

    vk_api_version = '5.131'
    user = None

    user_info = VkApi(token_vk, vk_api_version)
    # print(user_info.get_user(None))
    print(user_info.get_friends(None))
