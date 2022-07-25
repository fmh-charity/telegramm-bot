"""
initial create tables
"""

from yoyo import step

__depends__ = {"20220715_01_insert_initial_data"}


step("""INSERT INTO ui_form
("key", type_id, "sequence", value, "access")
VALUES (
'ui_main_page', 
(select id from ui_type where name = 'message'),
(select coalesce(max("sequence")+1, 1) seq from ui_form where "key" = 'ui_main_page'),
'Добро пожаловать в благотворительную разработку проекта.
Выберите раздел который вас интересует', NULL);
""")

step("""INSERT INTO ui_form ("key",type_id,"sequence",value, "access")
VALUES (
'test_app_credentials_button',
(select id from ui_type where name = 'button'),
(select coalesce(max("sequence")+1, 1) seq from ui_form where "key" = 'test_app_credentials_button'),
'login1/password1', NULL);
""")

