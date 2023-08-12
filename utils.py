import json
import requests

from prettytable import PrettyTable

from messages import text
from settings import token

headers = {'X-API-KEY': token}
base_url = 'https://api.kinopoisk.dev'

random_movie = '/v1/movie/random'
info = '/v1.3/movie/'
all_seas_epis = '/v1/season'
review = '/v1/review'


class Parser:
    """
    Класс, позволяющий создать json-файл, как результат парсинга стороннего API,
    а так же вывести информацию на экран.

    Attributes:
        count (int): позволяет вести подсчет количества вызовов метода
    """
    count = 0

    @staticmethod
    def parse_json(endpoint, prnt, id_movie='') -> dict:
        """
        Метод возвращает json-объект, как результат парсинга стороннего API.
        :param endpoint: эндпоинт, по которому производится запрос API.
        :param prnt: ключ id, по которому производится поиск если необходимо.
        :param id_movie: параметр, разрешающий вывод результата в консоль.
        """
        try:
            # Формирование запроса по входящим данным.
            third_param = id_movie if endpoint in ('/v1.3/movie/', '/v1/movie/') else ''
            url = ''.join([base_url, endpoint, third_param])
            querystring = {'movieId': id_movie} if id_movie else {}
            res: dict = requests.get(url=url, headers=headers, params=querystring).json()
            if prnt:
                res_prn = json.dumps(res, indent=4, ensure_ascii=False)
                print(res_prn)
        except Exception as ex:
            print(f'Ошибка парсинга {ex=}')
        else:
            return res

    def make_json(self, id_movie='', prnt=False) -> None:
        """
        Метод обновляет json-файл результатом парсинга API с разными эндпоинтами.
        :param id_movie: параметр, разрешающий вывод результата в консоль.
        :param prnt: ключ id, по которому производится поиск если необходимо.
        """
        # Создаем объект из дампа.
        with open('dumps/movies_info.json', 'r', encoding='utf-8') as file:
            dump_in: dict = json.load(file)
        # Получаем json объект из стороннего API.
        obj = self.parse_json(info, id_movie=id_movie, prnt=prnt) if id_movie else self.parse_json(random_movie,
                                                                                                   prnt=prnt)
        # Проверка соответствия типа полученного объекта obj и наличия в объекте ключа id.
        if isinstance(obj, dict) and (id_movie := obj.get('id', 0)):
            id_movie = str(id_movie)
            dump_temp = dict.fromkeys(['Общая информация о фильме'], obj)
            dump_temp.update(
                {'Информация о сезонах и эпизодах': self.parse_json(all_seas_epis, id_movie=id_movie, prnt=prnt)})
            dump_temp.update({'Отзывы зрителей': self.parse_json(review, id_movie=id_movie, prnt=prnt)})
            dump_in.update({id_movie: dump_temp})
            with open(f'dumps/movies_info.json', 'w', encoding='utf-8') as file:
                json.dump(dump_in, file, indent=4, ensure_ascii=False)
            self.count += 1
        else:
            print('По этому id ничего не найдено!')

    @staticmethod
    def get_json(prnt=False, id_movie=''):
        """
        Метод создает json объект из файла. При необходимости выводит результат на экран.
        """
        with open('dumps/movies_info.json', 'r', encoding='utf-8') as file:
            dump_in: dict = json.load(file)
            if id_movie:
                dump_in = dump_in.get(id_movie, {'message': 'По этому id ничего не найдено!'})
            if prnt:
                res: str = json.dumps(dump_in, indent=4, ensure_ascii=False)
                print(res)
        return dump_in

    @staticmethod
    def print_table(obj) -> None:
        """
        Метод формирует поля для вывода информации в табличном варианте.
        """

        # В данном списке формируются поля для таблицы. В случае длинных текстов, они обрезаются.
        list_mov = [[ind + 1,
                     key,
                     list(map(lambda x: x[:25] + '...' if len(x) > 25 else x, [str(obj[key][text]['name'])]))[0],
                     obj[key][text]['year'],
                     'да' if obj[key][text]['isSeries'] else 'нет',
                     obj[key][text]['votes'].get('kp', '-'),
                     list(map(lambda x: x[:75] + ' (...)' if len(x) > 75 else x,
                              [str(obj[key][text].get('description', ''))]))[0],
                     ', '.join(list(map(lambda x: x['name'] if x else '', obj[key][text]['countries'])))]
                    for ind, key in enumerate(obj.keys())]
        my_table = PrettyTable()
        my_table.field_names = ["id", "mov_id", "name", "year", "сериал", "голоса КП", "описание", "страна"]
        my_table.add_rows(list_mov)
        print(my_table)
