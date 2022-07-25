# telegram-bot
## Для запуска:
Перед запуском необходимо убедиться что существует папка logs.
Так же требуется заполнить параметры в файле config.py

### Database
Используется СУБД **PostgreSQL**
Для подключения к бот-апи телеграмма используется __aiogram 3.0.0b3__
Поскольку это бета-версия, для установки среды venv из requirements требуется добавить ключ -r:
```shell
/usr/local/bin/MyBot/venv/bin/pip3 install --pre -r /usr/local/bin/myBot/requirements.txt
```