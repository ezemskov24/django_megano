# Интернет-магазин MEGANO
***
![45.153.69.124_ru_ (1).png](..%2F..%2F..%2F%D0%97%D0%B0%D0%B3%D1%80%D1%83%D0%B7%D0%BA%D0%B8%2F45.153.69.124_ru_%20%281%29.png)
## Структура проекта
### Приложения
- account - личный кабинет, пользователи и продавцы
- adminsettings - административные настройки сайта 
- cart - добавление товаров в корзину и создание заказов
- catalog - каталог и отзывы
- discounts - применение скидок к товарам
- payments - сервис оплаты заказов
- products - товары, категории, характеристики


### Служебные файлы и дерриктории
- fixtures - фикстуры с тестовыми данными
- locale - локализация текстовых строк
- media - загружамые медиа-файлы
- static - статические файлы для веб-приложения
- templates - шаблоны веб-страниц
- .env.template - шаблон переменных окружения
- docker-compose.dev.yaml - настройки docker-compose для разработки
- docker-compose.yaml - настройки docker-compose для продакшн
- docker-entrypoint.sh - скрипт запуска контейнера Docker
- Dockerfile - описание образа Docker
- nginx.conf - конфигурация Nginx
- requirements.txt - зависимости Python

***

## Установка и запуск проекта

Склонировать проект:

```
git clone https://gitlab.skillbox.ru/pythondjango_team37/diplom.git
```
В репозитории хранится файл .env.template. Надо на его основе создать и заполнить файл .env 

Если необходимо загрузить тестовые данные, то в файле .env требуется указать:
```
load_test_data=True
```
При загрузке тестовых данных создается пять пользователей:

| E-mail                   | Пароль    | Категория     |
|--------------------------|-----------|---------------|
| admin@megano.com         | 123       | superuser     |
| seller_tony@megano.com   | qwaszx11  | Продавец      |
| seller_erlich@megano.com | qwaszx11  | Продавец      |
| manager@megano.com       | qwaszx11  | Администратор |
| walter@megano.com        | qwaszx11  | Покупатель    |
***
Перед запуском проекта необходимо собрать контейнер командой:
```
docker compose build
```

Запуск проекта: 
```
docker compose up -d
```
***
