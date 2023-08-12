from utils import *
from deco import timer
from messages import *

parse = Parser()


@timer
def main() -> None:
    """
    Функция позволяет заполнять базу данных в виде json информацией о фильмах из API Кинопоиска,
    заполнять ее по известному id, а так же вывести информацию из json файла как в исходном виде, так и в кратком
    табличном формате.
    """
    while True:
        print('\nВыберите желаемый пункт меню:')
        ask_1 = input(main_menu)
        if ask_1 == '1':
            numb = int(input('Введите количество запросов к API\n'))
            ask_2 = input(ask_print)
            [parse.make_json(prnt=ask_2 == '1') for _ in range(numb)]
            if parse.count:
                print(f'Количество записей в базе данных увеличено на {parse.count}\n')
                parse.count = 0
            else:
                print('База данных не была пополнена')
        elif ask_1 == '2':
            id_mov = input('Введите требуемый id\n')
            ask_2 = input(ask_print)
            parse.make_json(id_movie=id_mov, prnt=ask_2 == '1')
        elif ask_1 == '3':
            ask_2 = input('Будет выведена таблица с краткой информацией о фильмах.'
                          ' Если же хотите вывести все данные, введите 1, если только таблицу - любой символ\n')
            ask_3 = input('Введите для сортировки 1: по имени, 2: по году, 3: по типу, 4: по голосам, 5: по стране'
                          '\nБез сортировки - просто нажмите ввод\n')
            field_sort = ask_3 if ask_3 in ('1', '2', '3', '4', '5') else None
            res = parse.get_json(prnt=ask_2 == '1')
            print('Краткая информация о фильмах из базы данных:\n')
            parse.print_table(res, field_sort=field_sort)
            id_mov = input('Введите id, чтобы получить данные фильма из дампа. Выход - введите пробел\n')
            if id_mov:
                parse.get_json(prnt=True, id_movie=id_mov)
        else:
            break


if __name__ == '__main__':
    main()
