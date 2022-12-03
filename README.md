****
# Тестовое задание Mailganer

Написать на Python 2.7 (другие версии питона не принимаем) или GO небольшой сервис отправки имейл рассылок.
Возможности сервиса:
 1. Отправка рассылок с использованием html макета и списка подписчиков.
 2. Отправка отложенных рассылок.
 3. Использование переменных в макете рассылки. (Пример: имя, фамилия, день рождения из списка подписчиков)
 4. Отслеживание открытий писем.
Отложенные отправки реализовать при помощи Celery (актуально только для реализации на Python).

P.S.: Способ хранения макетов писем и списков подписчиков на усмотрение исполнителя.
****


- Так как ни каких чётких критериев не указано, то ограничился предположением, что пользователи сервиса имеете гуглопочту, от имени которой будет производиться рассылка.

>>*Прим. Google имеет ограничение 500 писем/день для частных аккаунтов.
Также Google не позоляет реализовать уведомления о прочтении для частных клиентов. Возможно, данная функция имеется в API, но реализацию этой функции оставил на последний этап и приложение уже было написано.*
- Авторизация клиетнов производиться путём проверки возможности рассылки с предоставленной почты, никаких данных, кроме необходимых для рассылки, не требуется.
- Список контактов можно загрузить оптом в CSV файле или добавлять по одному вручную.
- Переменные в письма вставляются посредством **Jinja2**.
- Рассылка и отложенная рассылка реализованы посредством **Celery+Redis**.
- Свежезарегистрированные пользователи имеют ограничение по рассылке для понуждения оплаты сервиса.

****
### Установка

*На вашей ЭВМ должен быть установлен `docker`*.

Создать директорию для приложения:
```
mkdir mailgun & cd mailgun
```
Создать файл `.env` и заполнить его:
```
nano .env
```
```
DATABASE_URI='sqlite:///db.sqlite3'
SECRET_KEY=Your2secret1key

CELERY_BROKER_URL='redis://localhost:6379/0'
DOCKER_REDIS_NAME=docker_redis
```
*Некоторые значение, в заисимости от выбранного способа запуска, не нужны*.



Скопировать в директорию `/mailgun/` файл `docker_compose.yml` и запустить его:
```
sudo docker-compose up
```
Дальше происходит магия и необходимые сервисы скачиваются и запускаются запускается (или нет :grinning:).


Также можно скачать только образ `Redis` или просто установить его.

А кроме того, вам понадобится `Python 2`.

Затем скачать весь этот проект:
```
git@github.com:Xewus/MailGun.git
```
Создать и активировать виртуальное окружение:
```
virtualenv venv 
```
```
. venv/bin/activate
```
Установить зависимости:
```
pip install -U pip | pip install -r requirements.txt
```
Запустить проект:
```
./start_app.py
```
И, наконец, третий вариант для не ленивых.

Запустить `Celery` в одном терминале:
```
celery worker -A src.celery_tasks.tasks -B -l info
```
Запустить проект во втором терминале:
```
 ./flask.py 
```


 

