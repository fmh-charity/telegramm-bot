"""
initial create tables
"""

from yoyo import step

__depends__ = {"20220710_01_initial_create_tables"}

step("""INSERT INTO ui_type ("name", description) VALUES('message', 'Текст сообщения');""")
step("""INSERT INTO ui_type ("name", description) VALUES('button', 'Кнопки');""")

step("""INSERT INTO users
(user_id, username, firstname, lastname, "access")
VALUES (4210135, 'isaroot', 'Сергей', '𝓲𝓼𝓪𝓻𝓸𝓸𝓽 ≈)', 100);
""")
step("""INSERT INTO users
(user_id, username, firstname, lastname, "access")
VALUES (931454208, NULL, 'Evgeni', NULL, NULL);
""")
step("""INSERT INTO users
(user_id, username, firstname, lastname, "access")
VALUES (276876990, 'angelinka_ru', 'Ангелина', NULL, NULL);
""")

step("""INSERT INTO ui_links
(url_key, url, "label")
VALUES ('figma_web_link', 'https://www.figma.com/file/mQmhIyt08ES3MdSNwOpYnS/%D0%9F%D0%B5%D1%80%D0%B2%D1%8B%D0%B9-%D0%BC%D0%BE%D1%81%D0%BA%D0%BE%D0%B2%D1%81%D0%BA%D0%B8%D0%B9-%D1%85%D0%BE%D1%81%D0%BF%D0%B8%D1%81%2C-%D0%B2%D0%B5%D0%B1-%D0%B2%D0%B5%D1%80%D1%81%D0%B8%D1%8F-%D0%BC%D0%B0%D0%BA%D0%B5%D1%82%D0%BE%D0%B2-%D0%BF%D1%80%D0%B8%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F', '🎨🌐 Фигма web');
""")
step("""INSERT INTO ui_links
(url_key, url, "label")
VALUES ('trello_frontend_link', 'https://trello.com/user34668309', '📊 Trello');
""")
step("""INSERT INTO ui_links
(url_key, url, "label")
VALUES ('github_frontend_link', 'https://github.com/fmh-charity/fmh-web', '📝 GitHub Web');
""")
step("""INSERT INTO ui_links
(url_key, url, "label")
VALUES ('chat_frontend', 'https://t.me/demirelkd', '💬 Доступ в чат разработчиков');
""")
step("""INSERT INTO ui_links
(url_key, url, "label")
VALUES ('frontend_access_link', 'https://t.me/demirelkd', '🔐 Запросить доступы');
""")
step("""INSERT INTO ui_links
(url_key, url, "label")
VALUES ('frontend_system_requirements_link', 'https://pmhproject.myjetbrains.com/youtrack/articles/pmh-A-1/%D0%91%D0%A2---%D0%A4%D0%A2', 'Требования к системе');
""")

step("""INSERT INTO ui_links
(url_key, url, "label")
VALUES ('chat_android', 'https://t.me/Dolgoff62', '💬 Доступ в чат разработчиков');
""")
step("""INSERT INTO ui_links
(url_key, url, "label")
VALUES ('github_android_link', 'https://github.com/fmh-charity/fmh-android', '📝 GitHub Android');
""")
step("""INSERT INTO ui_links
(url_key, url, "label")
VALUES ('trello_android_link', 'https://trello.com/b/0Q9cvmqs/android', '📊 Trello');
""")
step("""INSERT INTO ui_links
(url_key, url, "label")
VALUES ('figma_android_link', 'https://www.figma.com/file/mQmhIyt08ES3MdSNwOpYnS/%D0%9F%D0%B5%D1%80%D0%B2%D1%8B%D0%B9-%D0%BC%D0%BE%D1%81%D0%BA%D0%BE%D0%B2%D1%81%D0%BA%D0%B8%D0%B9-%D1%85%D0%BE%D1%81%D0%BF%D0%B8%D1%81%2C-%D0%B2%D0%B5%D0%B1-%D0%B2%D0%B5%D1%80%D1%81%D0%B8%D1%8F-%D0%BC%D0%B0%D0%BA%D0%B5%D1%82%D0%BE%D0%B2-%D0%BF%D1%80%D0%B8%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F?node-id=182%3A312', '🎨📱 Фигма Android');
""")
step("""INSERT INTO ui_links
(url_key, url, "label")
VALUES ('android_access_link', 'https://t.me/Dolgoff62', '🔐 Запросить доступы');
""")
step("""INSERT INTO ui_links
(url_key, url, "label")
VALUES ('android_knowledge_base_link', 'https://pmhproject.myjetbrains.com/youtrack/articles/pmh-A-29/%D0%9E%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5-%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%B0', '📚 База знаний');
""")

step("""INSERT INTO ui_links
(url_key, url, "label")
VALUES ('chat_ios', 'https://t.me/omsklain', '💬 Доступ в чат разработчиков');
""")
step("""INSERT INTO ui_links
(url_key, url, "label")
VALUES ('trello_ios_link', 'https://trello.com/b/W3mOxvrm/ios', '📊 Trello');
""")
step("""INSERT INTO ui_links
(url_key, url, "label")
VALUES ('github_ios_link', 'https://github.com/fmh-charity/fmh-ios', '📝 GitHub IOS');
""")
step("""INSERT INTO ui_links
(url_key, url, "label")
VALUES ('figma_ios_link', 'https://www.figma.com/file/hrEVEevntzZfS0AYBNjb7q/%D0%9F%D0%B5%D1%80%D0%B2%D1%8B%D0%B9-%D0%BC%D0%BE%D1%81%D0%BA%D0%BE%D0%B2%D1%81%D0%BA%D0%B8%D0%B9-%D1%85%D0%BE%D1%81%D0%BF%D0%B8%D1%81%2C-%D0%B2%D0%B5%D1%80%D1%81%D0%B8%D1%8F-%D0%BC%D0%B0%D0%BA%D0%B5%D1%82%D0%BE%D0%B2-%D0%BF%D1%80%D0%B8%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F-%D0%B4%D0%BB%D1%8F-IOS', '🎨📱 Фигма IOS');
""")
step("""INSERT INTO ui_links
(url_key, url, "label")
VALUES ('ios_system_requirements_link', 'https://pmhproject.myjetbrains.com/youtrack/articles/pmh-A-1/%D0%91%D0%A2---%D0%A4%D0%A2', 'Требования к системе');
""")
step("""INSERT INTO ui_links
(url_key, url, "label")
VALUES ('ios_access_link', 'https://t.me/omsklain', '🔐 Запросить доступы');
""")
step("""INSERT INTO ui_links
(url_key, url, "label")
VALUES ('ios_knowledge_base_link', 'https://pmhproject.myjetbrains.com/youtrack/articles/pmh-A-29/%D0%9E%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5-%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%B0', '📚 База знаний');
""")
step("""INSERT INTO ui_links
(url_key, url, "label")
VALUES ('ios_TestFlight_link', 'get_test_flight_app', '✈️ TestFlight');
""")

step("""INSERT INTO ui_links
(url_key, url, "label")
VALUES ('chat_backend', 'https://t.me/Dimon_Donskoi', '💬 Доступ в чат разработчиков');
""")
step("""INSERT INTO ui_links
(url_key, url, "label")
VALUES ('trello_backend_link', 'https://trello.com/b/d8oSGyfz/backend', '📊 Trello');
""")
step("""INSERT INTO ui_links
(url_key, url, "label")
VALUES ('github_backend_link', 'https://github.com/fmh-charity/fmh-backend', '📝 GitHub Backend');
""")
step("""INSERT INTO ui_links
(url_key, url, "label")
VALUES ('figma_backend_link', 'https://www.figma.com/file/Vhm1DfDr6UIecVycvWG3fh/%D0%9F%D0%B5%D1%80%D0%B2%D1%8B%D0%B9-%D0%BC%D0%BE%D1%81%D0%BA%D0%BE%D0%B2%D1%81%D0%BA%D0%B8%D0%B9-%D1%85%D0%BE%D1%81%D0%BF%D0%B8%D1%81%2C-%D0%BC%D0%BE%D0%B1%D0%B8%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F-%D0%B2%D0%B5%D1%80%D1%81%D0%B8%D1%8F-%D0%BC%D0%B0%D0%BA%D0%B5%D1%82%D0%BE%D0%B2-%D0%BF%D1%80%D0%B8%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F?node-id=807%3A1244', '🎨🔙🔚 Фигма Backend');
""")
step("""INSERT INTO ui_links
(url_key, url, "label")
VALUES ('backend_access_link', 'https://t.me/Dimon_Donskoi', '🔐 Запросить доступы');
""")
step("""INSERT INTO ui_links
(url_key, url, "label")
VALUES ('backend_knowledge_base_link', 'https://pmhproject.myjetbrains.com/youtrack/articles/pmh-A-29/%D0%9E%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5-%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%B0', '📚 База знаний');
""")

step("""INSERT INTO ui_links
(url_key, url, "label")
VALUES ('analytics_knowledge_base', 'https://pmhproject.myjetbrains.com/youtrack/articles/pmh-A-69/%D0%90%D0%BD%D0%B0%D0%BB%D0%B8%D1%82%D0%B8%D0%BA%D0%B0', '📚 База знаний');
""")
step("""INSERT INTO ui_links
(url_key, url, "label")
VALUES ('chat_analytics', 'https://t.me/AlisaKostiukova', '💬 Доступ в чат аналитиков');
""")
step("""INSERT INTO ui_links
(url_key, url, "label")
VALUES ('analytics_request_access', 'https://t.me/AlisaKostiukova', '🔐 Запросить доступ');
""")
step("""INSERT INTO ui_links
(url_key, url, "label")
VALUES ('trello_analytics_link', 'https://trello.com/b/RGdKst37/%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D1%82%D0%B8%D0%BA%D0%B0', '📊 Trello');
""")

step("""INSERT INTO ui_links
(url_key, url, "label")
VALUES ('github_main_link', 'https://github.com/fmh-charity/', '📝 GitHub');
""")
step("""INSERT INTO ui_links
(url_key, url, "label")
VALUES ('test_app_credentials_request', 'get_test_cred', '🔐 Запросить УЗ');
""")
step("""INSERT INTO ui_links
(url_key, url, "label")
VALUES ('swagger_link', 'https://test.vhospice.org/api/fmh/swagger-ui/#/', '🧑‍💻 Swagger');
""")
step("""INSERT INTO ui_links
(url_key, url, "label")
VALUES ('test_web_app_link', 'https://test.vhospice.org/login', '♨️ Тестовое web приложение');
""")
step("""INSERT INTO ui_links
(url_key, url, "label")
VALUES ('app_prod_link', 'https://fmh.vhospice.org/login', '🔞 web приложение (прод)');
""")
step("""INSERT INTO ui_links
(url_key, url, "label")
VALUES ('prod_map_miro_link', 'https://miro.com/app/board/o9J_kwHZYfE=/', 'В Хосписе (карта продукта)');
""")
# step("""INSERT INTO ui_links
# (url_key, url, "label")
# VALUES ('trello_main_link', 'https://trello.com/ru/iteco', '📊 Trello');
# """)
# step("""INSERT INTO ui_links
# (url_key, url, "label")
# VALUES ('figma_main_link', 'https://www.figma.com/iteco', '🎨 Фигма');
# """)

step("""INSERT INTO ui_links
(url_key, url, "label")
VALUES ('about_lenta_ru_01', 'https://lenta.ru/articles/2022/02/11/hospapp/', '📰 О проекте на Lenta.ru');
""")
step("""INSERT INTO ui_links
(url_key, url, "label")
VALUES ('about_iteco_inno_ru_01', 'https://www.iteco-inno.ru/social-projects', '📰 Сайт проекта');
""")


