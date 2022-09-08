# telegram-bot
## Для запуска:
Перед запуском необходимо убедиться что существует папка logs.\
Для запуска требуется заполнить и добавить следующие данные в переменные окружения:
```python
TOKEN = '0000000000:ABCDEFGHabcdefgh'  # полученный у @BotFather

pg_db_user = 'postgre_username'
pg_db_password = 'postgre_password'
pg_db_host = 'postgre_host'
pg_db_port = '5432'
pg_db_database = 'postgre_db_name'
pg_db_schema = 'postgre_schema_name'

bot_owner_id = 000000000

```
### Database
Используется СУБД **PostgreSQL**\
Для подключения к бот-апи телеграмма используется __aiogram 3.0.0b3__\

Для запуска не через докер может потребоваться следующее:\
Поскольку это бета-версия, для установки среды venv из requirements требуется добавить ключ -r:
```shell
/usr/local/bin/MyBot/venv/bin/pip3 install --pre -r /usr/local/bin/myBot/requirements.txt
```