from threading import Lock
import logging
from logging.config import fileConfig

import psycopg2
from psycopg2 import OperationalError
from psycopg2.extras import DictCursor

from bot import config

fileConfig('logging.ini', disable_existing_loggers=False)
log = logging.getLogger(__name__)


# def pg_conn(func):
#     def wrapper(*args, **kwargs):
#         with psycopg2.connect(user=config.pg_db_user, password=config.pg_db_password,
#                               host=config.pg_db_host, port=config.pg_db_port,
#                               dbname=config.pg_db_database, ) as conn:
#             with conn.cursor() as cursor:
#                 func(cursor, *args, **kwargs)
#
#
# # @pg_conn
# def get_test_value(cursor, lang, type, key):
#     sql = '''select ui.value from ui_form ui
#     where ui.lang_id = %s
#     and ui.type_id = %s
#     and ui.key_id = %s'''
#     cursor.execute(sql, (lang, type, key))
#     return cursor.fetchone()


class SingletonMeta(type):
    """
    Это потокобезопасная реализация класса Singleton.
    """

    _instances = {}

    _lock: Lock = Lock()
    """
    У нас теперь есть объект-блокировка для синхронизации потоков во время
    первого доступа к Одиночке.
    """

    def __call__(cls, *args, **kwargs):
        """
        Данная реализация не учитывает возможное изменение передаваемых
        аргументов в `__init__`.
        """
        # Теперь представьте, что программа была только-только запущена.
        # Объекта-одиночки ещё никто не создавал, поэтому несколько потоков
        # вполне могли одновременно пройти через предыдущее условие и достигнуть
        # блокировки. Самый быстрый поток поставит блокировку и двинется внутрь
        # секции, пока другие будут здесь его ожидать.
        with cls._lock:
            # Первый поток достигает этого условия и проходит внутрь, создавая
            # объект-одиночку. Как только этот поток покинет секцию и освободит
            # блокировку, следующий поток может снова установить блокировку и
            # зайти внутрь. Однако теперь экземпляр одиночки уже будет создан и
            # поток не сможет пройти через это условие, а значит новый объект не
            # будет создан.
            if cls not in cls._instances:
                cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
                # cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Singleton(metaclass=SingletonMeta):
    db = psycopg2.connect(user=config.pg_db_user, password=config.pg_db_password,
                          host=config.pg_db_host, port=config.pg_db_port,
                          dbname=config.pg_db_database, options=f'-c search_path={config.pg_db_schema}')

    def __init__(self):
        log.info('----db init is started----')

        log.info('----db init is ended----')

    def users_add_new_on_start(self, user_id, username, firstname, lastname):
        sql = '''INSERT INTO users
        (user_id, username, firstname, lastname) 
        values (%s, %s, %s, %s)        
        ON CONFLICT (user_id) DO NOTHING;
        '''
        try:
            with self.db as conn:
                data = [user_id, username, firstname, lastname]
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()
        except OperationalError:
            log.exception(f"Ошибка добавления пользователя: '{username}' в таблицу 'users'")

    def users_get_by_uid(self, user_id):
        sql = '''SELECT user_id, username, firstname, lastname, access
        FROM users
        where user_id = %s
        '''
        try:
            with self.db as conn:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    data = [user_id]
                    cursor.execute(sql, data)
                    res = cursor.fetchone()
        except OperationalError:
            log.exception(f"Ошибка поиска пользователя: '{user_id}' в таблице 'users'")
        else:
            return res

    def group_chat_get_by_id(self, chat_id):
        sql = """SELECT chat_id, linked_chat_id, chat_title, chat_fullname, chat_description, chat_type
                    from group_chat where chat_id = %s
                    """
        try:
            with self.db as conn:
                data = [chat_id]
                cursor = conn.cursor()
                cursor.execute(sql, data)
                res = cursor.fetchone()
        except OperationalError:
            log.exception(f"Ошибка запроса чата: '{chat_id}' из таблицы 'group_chat'")
        else:
            return res

    def group_chat_add_new(self, chat_id, linked_chat_id, chat_title, chat_fullname, chat_description, chat_type):
        sql = '''INSERT INTO group_chat 
        (chat_id, linked_chat_id, chat_title, chat_fullname, chat_description, chat_type) 
        values (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (chat_id) DO NOTHING;
        '''
        try:
            with self.db as conn:
                data = [chat_id, linked_chat_id, chat_title, chat_fullname, chat_description, chat_type]
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()
                log.info(f"чат добавлен: '{chat_title}({chat_id})' в таблицу 'group_chat'")
                pass
        except OperationalError:
            log.exception(f"Ошибка добавления чата: '{chat_title}({chat_id})' в таблицу 'group_chat'")

    def group_chat_update(self, chat_id, linked_chat_id, chat_title, chat_fullname, chat_description, chat_type):
        sql = '''UPDATE group_chat SET
        linked_chat_id = %s, chat_title = %s, chat_fullname = %s, chat_description = %s,
        chat_type = %s
        WHERE chat_id = %s
        '''
        try:
            with self.db as conn:
                data = [linked_chat_id, chat_title, chat_fullname, chat_description, chat_type, chat_id]
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()
                log.info(f"чат обновлен: '{chat_title}({chat_id})' в таблице 'group_chat'")
        except OperationalError:
            log.exception(f"Ошибка обновления чата: '{chat_title}({chat_id})' в таблице 'group_chat'")

    def group_chat_update_on_upgrade_group(self, chat_id, new_chat_id):
        sql = '''UPDATE group_chat SET chat_id = %s
        WHERE chat_id = %s
        '''
        try:
            with self.db as conn:
                data = [new_chat_id, chat_id]
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()
                log.info(f"чат обновлен: {chat_id}=>{new_chat_id}' в таблице 'group_chat'")
        except OperationalError:
            log.exception(f"Ошибка обновления чата: '{chat_id}=>{new_chat_id}' в таблице 'group_chat'")

    def group_chat_delete(self, chat_id):
        sql = '''DELETE FROM group_chat
        WHERE chat_id = %s
        '''
        try:
            with self.db as conn:
                data = [chat_id]
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()
                log.info(f"удален чат {chat_id}' из таблицы 'group_chat'")
        except OperationalError:
            log.exception(f"Ошибка удаления чата: '{chat_id}' из таблицы 'group_chat'")

    def ui_links_get_by_key(self, key):
        sql = '''SELECT id, url_key, url, "label"
            FROM ui_links
            where url_key = %s;
            '''
        try:
            with self.db as conn:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    cursor.execute(sql, (key,))
                    res = cursor.fetchone()
        except OperationalError:
            log.exception(f"Ошибка запроса ссылки по ключу: '{key}' из таблицы 'ui_links'")
        else:
            return res

    def ui_links_get_by_id(self, link_id):
        sql = '''SELECT id, url_key, url, "label"
            FROM ui_links
            where id = %s;
            '''
        try:
            with self.db as conn:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    cursor.execute(sql, (link_id,))
                    res = cursor.fetchone()
        except OperationalError:
            log.exception(f"Ошибка запроса ссылки по id: '{link_id}' из таблицы 'ui_links'")
        else:
            return res

    def ui_links_get_next_key_list(self, start_id):
        sql = '''SELECT id, url_key, url, "label"
            FROM ui_links
            where id > %s
            order by id
            limit 10
            '''
        try:
            with self.db as conn:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    data = [start_id]
                    cursor.execute(sql, data)
                    res = cursor.fetchall()
        except OperationalError:
            log.exception(f"Ошибка запроса ключей ссылок с id > '{start_id}' из таблицы 'ui_links'")
        else:
            return res

    def ui_links_get_prev_key_list(self, start_id):
        sql = '''select * from(
            SELECT id, url_key, url, "label"
                FROM ui_links ul
                where ul.id < %s
                order by ul.id desc
                limit 10) uli
            order by uli.id asc
            '''
        try:
            with self.db as conn:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    data = [start_id]
                    cursor.execute(sql, data)
                    res = cursor.fetchall()
        except OperationalError:
            log.exception(f"Ошибка запроса ключей ссылок с id < '{start_id}' из таблицы 'ui_links'")
        else:
            return res

    def ui_links_get_min_max_id(self):
        sql = '''SELECT min(id), max(id)
            FROM ui_links
            '''
        try:
            with self.db as conn:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    cursor.execute(sql)
                    res = cursor.fetchone()
        except OperationalError:
            log.exception(f"Ошибка запроса минимального и максимального id из таблицы 'ui_links'")
        else:
            return res

    def ui_links_update_url_by_id(self, l_id, url):
        sql = '''UPDATE ui_links SET
        url = %s
        WHERE id = %s
        '''
        try:
            with self.db as conn:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    data = [url, l_id]
                    cursor.execute(sql, data)
                    conn.commit()
                    log.info(f"URL с ID = {l_id} изменен на '{url}' в таблице 'ui_links'")
        except OperationalError:
            log.exception(f"Ошибка изменения URL с ID = {l_id} на '{url}' в таблице 'ui_links'")

    def ui_links_update_label_by_id(self, l_id, label):
        sql = '''UPDATE ui_links SET
        label = %s
        WHERE id = %s
        '''
        try:
            with self.db as conn:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    data = [label, l_id]
                    cursor.execute(sql, data)
                    conn.commit()
                    log.info(f"label с ID = {l_id} изменен на '{label}' в таблице 'ui_links'")
        except OperationalError:
            log.exception(f"Ошибка изменения label с ID = {l_id} на '{label}' в таблице 'ui_links'")

    def ui_links_add_new_link(self, l_key, url, label):
        sql = '''INSERT INTO users
                (url_key, url, "label") 
                values (%s, %s, %s)        
                ON CONFLICT (url_key) DO NOTHING;
                '''
        try:
            with self.db as conn:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    data = [l_key, url, label]
                    cursor.execute(sql, data)
                    conn.commit()
                    log.info(f"Добавлена новая ссылка: label = '{label}' в таблицу 'ui_links'")
        except OperationalError:
            log.exception(f"Ошибка добавления ссылки с label = {label} в таблицу 'ui_links'")

    def ui_form_get_next_key_list(self, start_id):
        sql = '''select max(id) id, uf.key, min(uf.type_id) "type_id", count(uf.sequence) "sequence",
                min(uf.value) "value", min(uf.access) "access"
                FROM ui_form uf
                where id > %s
                group by uf.key
                order by id asc
                limit 10
            '''
        try:
            with self.db as conn:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    data = [start_id]
                    cursor.execute(sql, data)
                    res = cursor.fetchall()
        except OperationalError:
            log.exception(f"Ошибка запроса ключей ссылок с id > '{start_id}' из таблицы 'ui_form'")
        else:
            return res

    def ui_form_get_prev_key_list(self, start_id):
        sql = '''select * from(
                    select min(id) id, uf.key, min(uf.type_id) "type_id", count(uf.sequence) "sequence",
                    min(uf.value) "value", min(uf.access) "access"
                    FROM ui_form uf
                    where id < %s
                    group by uf.key
                    order by id desc
                limit 10) uli
            order by uli.id asc
            '''
        try:
            with self.db as conn:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    data = [start_id]
                    cursor.execute(sql, data)
                    res = cursor.fetchall()
        except OperationalError:
            log.exception(f"Ошибка запроса ключей ссылок с id < '{start_id}' из таблицы 'ui_form'")
        else:
            return res

    def ui_form_get_min_max_id(self):
        sql = '''SELECT min(id), max(id)
            FROM ui_form
            '''
        try:
            with self.db as conn:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    cursor.execute(sql)
                    res = cursor.fetchone()
        except OperationalError:
            log.exception(f"Ошибка запроса минимального и максимального id из таблицы 'ui_form'")
        else:
            return res

    def ui_form_get_values_by_key(self, key):
        sql = '''select uf.id, uf.key, uf.type_id, uf.sequence,
                uf.value, uf.access
                FROM ui_form uf
                where uf.key = %s
                order by uf.sequence asc;
            '''
        try:
            with self.db as conn:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    data = [key]
                    cursor.execute(sql, data)
                    res = cursor.fetchall()
        except OperationalError:
            log.exception(f"Ошибка запроса данных по ключу '{key}' из таблицы 'ui_form'")
        else:
            return res
