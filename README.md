# Парсинг API с Кинопоиска
Программа парсит API Кинопоиска по следующим эндпоинтам:
1. Выбрать рандомного фильма: /v1/movie/random
2. Получить всю информацию о фильме: /v1/movie/{id}
3. Получить все сезоны и эпизоды: /v1/season
4. Отзывы пользователей: /v1/review
Результаты агрегируются в словарь, где по ключам id фильмов собрана вся информация о них с данного API.
Затем словарь сериализуется в json файл.

При запуске появляется меню:
```
Выберите желаемый пункт меню:
1. Пополнить базу данных фильмов случайной выборкой из API "Кинопоиска" - введите 1
2. Получить данные фильма по известному вам id и внести его в базу данных - введите 2
3. Получить информацию обо всех сохраненных в базе данных фильмов - введите 3
Выход - любой другой символ
```

При выборе пункта 1 нужно ввести количество фильмов, которые будут внесены в базу данных json по итогам парсинга
При выборе пункта 2 нужно указать id фильма, который при успешно поиске будет внесен в файл json
При выборе пункта 3 можно вывести на экран таблицу с краткой информацией о уже сохраненных филльмах, а после произвести поиск по локальной базе данных, 
указав id фильма. Реализована возможность сортировки по наименованию полей.
Во всех случаях программа запросит разрешение вывода на экран результата поиска в формате словаря.  
