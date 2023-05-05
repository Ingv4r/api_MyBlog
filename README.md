# Описание проекта
API для приложения yatube. Ответы в формате JSON. Применены пермишены, пагинация и фильтрация ответов API
# Как запустить проект:
1. Клонировать репозиторий, если к нему есть доступ и перейти в него в командной строке:
```
git clone https://github.com/Ingv4r/api_final_yatube.git
```
```
cd api_final_yatube/
```
2. Cоздать и активировать виртуальное окружение: 
>В проекте использовалась версия python 3.9.0
```
py -3.9 -m venv env
```
```
source env/bin/activate
```
3. Установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
4. Выполнить миграции:
```
python manage.py migrate
```
5. Запустить проект:
```
python3 manage.py runserver
```
# Примеры запросов
> SAVE методы могут посылать анонимные пользователи
## Получение JWT токена аутентификации для зарегистрированного польхователя:
```
POST http://127.0.0.1:8000/api/v1/jwt/create/
Content-Type: application/json

{
  "username": "string",
  "password": "string"
}
```
## Получение списка публикаций:
```
GET http://127.0.0.1:8000/api/v1/posts/
```
## Получение конкретной публикации по id:
```
GET http://127.0.0.1:8000/api/v1/posts/{id}/
```
## Создание поста:
```
POST http://127.0.0.1:8000/api/v1/posts/
Authorization: Bearer <your_token>
Content-Type: application/json

{
  "text": "string",
  "image": "string",
  "group": 1
}
```
## Получение комментариев:
```
GET http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/
```
## Получение комментария:
```
GET http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/{comment_id}/
```
## Получение списка сообществ:
```
GET http://127.0.0.1:8000/api/v1/groups/
```
## Получение списка подписок авторизованного пользователя
> Только аутентифицированные пользователи могут делать запросы к этому эндпоинту.
```
GET http://127.0.0.1:8000/api/v1/follow/
Authorization: Bearer <your_token>
```
