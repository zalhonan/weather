### Сервис для информирования о погоде по городам

API отвечает на HTTP-запрос `GET /weather?city=<city_name>`,
где `<city_name>` - это название города на английском языке.

Возвращает текущую температуру в этом городе в градусах Цельсия, атомсферное давление (мм рт.ст.) и скорость ветра (м/c) в формате json.

Cервис получает данные о погоде от [openweathermap](http://openweathermap.com), при последующих запросах для этого города в течение получаса предоставляются сохраненные данные из базы, запросы на сервис openweathermap.com не идут.

Инструкция по запуску:

1. Установите python 3
2. Установите пакеты по списку requirements.txt
3. Получите API ключ [openweathermap](http://openweathermap.com)
4. Пропишите ключ в файле env_sample.py, переименуйте его в env.py
5. Запустите app.py как обычное приложение Flask
6. Запуск локального сервера: python app.py
7. Наслаждайтесь прогнозом погоды в json формате по городам!