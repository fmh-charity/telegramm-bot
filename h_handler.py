import logging
from logging.config import fileConfig

from aiogram import Router, types, F
from aiogram.dispatcher.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from psycopg2.extras import DictRow

import postgre_db
from h_cb_data import CallbackPage

fileConfig('logging.ini', disable_existing_loggers=False)
log = logging.getLogger(__name__)
router = Router()
db = postgre_db.Singleton()


def get_start_buttons():
    builder = ReplyKeyboardBuilder()
    line1 = []
    line2 = []
    line3 = []
    line4 = []
    design_button = types.KeyboardButton(text='🧑‍🎨 Дизайн')
    analytics_button = types.KeyboardButton(text='📈 Аналитика')
    # chat_button = types.KeyboardButton(text='📟 Общий чат')
    owner_button = types.KeyboardButton(text='📟 Владелец продукта')
    line1.append(design_button)
    line1.append(analytics_button)
    line1.append(owner_button)
    # line1.append(chat_button)
    builder.row(*line1)
    map_button = types.KeyboardButton(text='🗺 Карта продукта')
    line2.append(map_button)
    # trello_button = types.KeyboardButton(text='📊 Trello')
    # line2.append(trello_button)
    about_button = types.KeyboardButton(text='™️ О проекте')
    line2.append(about_button)
    builder.row(*line2)
    develop_button = types.KeyboardButton(text='🛠 Разработка')
    github_button = types.KeyboardButton(text='📝 GitHub')
    line3.append(develop_button)
    line3.append(github_button)
    builder.row(*line3)
    # swagger_button = types.KeyboardButton(text='Swagger')
    test_cred_button = types.KeyboardButton(text='🔐 Учетка для тестового приложения')
    line4.append(test_cred_button)
    builder.row(*line4)

    return builder.as_markup(resize_keyboard=True)


def get_develop_buttons():
    builder = ReplyKeyboardBuilder()
    line1 = []
    line2 = []
    line3 = []
    line4 = []
    web_button = types.KeyboardButton(text='🌐 Web')
    backend_button = types.KeyboardButton(text='🔙🔚 Backend')
    line1.append(web_button)
    line1.append(backend_button)
    builder.row(*line1)
    ios_button = types.KeyboardButton(text='📱 ios разработка')
    android_button = types.KeyboardButton(text='📱 android разработка')
    line2.append(ios_button)
    line2.append(android_button)
    builder.row(*line2)
    swagger_button = types.KeyboardButton(text='🧑‍💻 Swagger Test')
    github_button = types.KeyboardButton(text='📝 GitHub')
    line3.append(swagger_button)
    line3.append(github_button)
    builder.row(*line3)
    main_back_button = types.KeyboardButton(text='🏚 На главную')
    line4.append(main_back_button)
    builder.row(*line4)

    return builder.as_markup(resize_keyboard=True)


@router.callback_query(CallbackPage.filter(F.action == 'main'))
async def analytics_page_callback(call: types.CallbackQuery):
    await call.answer('🏚 На главную')
    await bot_main_page_handler(call.message)


@router.message(F.chat.type == 'private', F.text == '🏚 На главную')
@router.message(F.chat.type == 'private', Command(commands="start"))
async def bot_main_page_handler(message: types.Message):
    text = 'Добро пожаловать в команду разработчиков приложения для хосписа!\n'
    text += 'Выберите раздел, который вас интересует.'
    mc = message.chat
    uid = mc.id
    # id, user_id, main_uid, username, name, squad_id, squad_tag, squad_name
    user = db.users_get_by_uid(uid)
    if user is None:
        db.users_add_new_on_start(uid, mc.username, mc.first_name, mc.last_name)
    await message.answer(text, reply_markup=get_start_buttons())


@router.message(F.chat.type == 'private', Command(commands="buttons"))
async def bot_main_page_handler(message: types.Message):
    text = '⌨️Кнопочки.\n'
    mc = message.chat
    uid = mc.id
    # id, user_id, main_uid, username, name, squad_id, squad_tag, squad_name
    user = db.users_get_by_uid(uid)
    if user is None:
        db.users_add_new_on_start(uid, mc.username, mc.first_name, mc.last_name)
    await message.answer(text, reply_markup=get_start_buttons())


@router.message(F.chat.type == 'private', F.text == '🧑‍🎨 Дизайн')
async def design_page_handler(message: types.Message):
    text = '🧑‍🎨 Дизайн.\n\n'
    text += 'Выберите ссылку которая вас интересует'
    # три кнопки-ссылки на фигмы
    builder = InlineKeyboardBuilder()
    link_keys = ['figma_web_link', 'figma_backend_link', 'figma_ios_link', 'figma_android_link']
    for key in link_keys:
        # id, url_key, url, "label"
        link_fdb: DictRow = db.ui_links_get_by_key(key)
        target_text = link_fdb.get('label')
        target_link = link_fdb.get('url')
        button = types.InlineKeyboardButton(text=target_text, url=target_link)
        builder.row(button)
    await message.answer(text, reply_markup=builder.as_markup())


@router.message(F.chat.type == 'private', F.text == '📈 Аналитика')
async def analytics_page_handler(message: types.Message):
    text = '📈 Аналитика.\n\n'
    text += 'Выберите ссылку которая вас интересует'
    # три кнопки-ссылки на фигмы
    builder = InlineKeyboardBuilder()
    builder.adjust(2)
    link_keys = ['analytics_knowledge_base', 'analytics_request_access', 'chat_analytics', 'trello_analytics_link',
                 'prod_map_miro_link']
    for key in link_keys:
        # id, url_key, url, "label"
        link_fdb: DictRow = db.ui_links_get_by_key(key)
        target_text = link_fdb.get('label')
        target_link = link_fdb.get('url')
        button = types.InlineKeyboardButton(text=target_text, url=target_link)
        builder.row(button)
    # analytics_button = types.InlineKeyboardButton(text='✅ Аналитика',
    #                                               callback_data=CallbackPage(action='analytics').pack())
    # builder.add(analytics_button)
    # map_button = types.InlineKeyboardButton(text='🗺 Карта продукта',
    #                                         callback_data=CallbackPage(action='prod_map').pack())
    # builder.add(map_button)
    await message.answer(text, reply_markup=builder.as_markup())


@router.callback_query(CallbackPage.filter(F.action == 'analytics'))
async def analytics_page_callback(call: types.CallbackQuery):
    text = 'Что-то на аналитическом'
    await call.message.answer(text, reply_markup=get_start_buttons())
    await call.answer('✅ Аналитика')


@router.callback_query(CallbackPage.filter(F.action == 'prod_map'))
async def prod_map_page_callback(call: types.CallbackQuery):
    await call.answer('🗺 Карта продукта')
    await product_map_page_handler(call.message)


@router.message(F.chat.type == 'private', F.text == '📟 Владелец продукта')
async def product_owner_page_handler(message: types.Message):
    text = 'Владелец продукта:\n'
    text += 'Что-то о владельце продукта'
    await message.answer(text, reply_markup=get_start_buttons())


@router.message(F.chat.type == 'private', F.text == '🗺 Карта продукта')
async def product_map_page_handler(message: types.Message):
    text = '🗺 Карта продукта\n'
    text += 'Чтобы получить информацию о карте продукта проследуйте по кнопке ниже'
    builder = InlineKeyboardBuilder()
    builder.adjust(2)
    link_keys = ['prod_map_miro_link']
    for key in link_keys:
        # id, url_key, url, "label"
        link_fdb: DictRow = db.ui_links_get_by_key(key)
        target_text = link_fdb.get('label')
        target_link = link_fdb.get('url')
        button = types.InlineKeyboardButton(text=target_text, url=target_link)
        builder.row(button)
    await message.answer(text, reply_markup=builder.as_markup())


@router.message(F.chat.type == 'private', F.text == '™️ О проекте')
async def about_page_handler(message: types.Message):
    text = '''™️ О проекте

Приложение "В хосписе" это единое информационное пространство для сотрудников хосписа и волонтеров, пациентов и их родственников.
Приложение содержит в себе полезные инструменты для организации внутренних коммуникаций: от размещения новостей о жизни хосписа до постановки задач и трекинга времени выполнения.
«В хосписе» позволяет избавиться от рутины в процессах коммуникации.

*Узнавать о важных событиях в жизни хосписа
*Оповещать сотрудников об изменениях в рабочих процессах
*Координировать работу волонтеров
*Оперативно обменивайтесь информацией
*Контролировать выполнение поставленных задач
*Отслеживать сроки выполнения 
*Обрабатывать просьбы пациентов. 

Получена лицензия о государственной регистрации программы ЭВМ №2021669868'''
    builder = ReplyKeyboardBuilder()
    builder.button(text='ℹ️Узнать о приложении больше')
    builder.button(text='👨‍👨‍👦‍👦 О команде')
    builder.button(text='🗽 Об Open Source')
    builder.button(text='🛠 Техническая составляющая')
    builder.button(text='🏚 На главную')
    builder.adjust(2)
    await message.answer(text, reply_markup=builder.as_markup(resize_keyboard=True))


@router.message(F.chat.type == 'private', F.text == '👨‍👨‍👦‍👦 О команде')
async def about_team_handler(message: types.Message):
    text = '''👨‍👨‍👦‍👦 О команде

В децентрализованную команду входят: РП, разработчики, тестировщики, аналитики, дизайнеры.
Верим, что созидание может быть бескорыстным.
Проект создается в свободное время на безвозмездной основе. 

Если ты готов развивать, вкладывать знания и делать удобный сервис, присоединяйся!
Будем рады видеть тебя в нашей команде!
'''
    await message.answer(text)


@router.message(F.chat.type == 'private', F.text == '🗽 Об Open Source')
async def about_opensource_handler(message: types.Message):
    text = '''🗽 Об Open Source

Приложение «В хосписе» создается на базе Open Source.
Продукт созданный  на открытом коде, распространяется свободно, без ограничений.
Любой желающий может присоединиться к проекту, внести свой вклад в разработку произведения создаваемого на безвозмездной основе.
'''
    await message.answer(text)


@router.message(F.chat.type == 'private', F.text == '🛠 Техническая составляющая')
async def about_tech_component_handler(message: types.Message):
    text = '''🛠 Техническая составляющая

В нашей уникальной децентрализованной команде - специалисты разных направлений
'''
    await message.answer(text)


@router.message(F.chat.type == 'private', F.text == 'ℹ️Узнать о приложении больше')
async def about_page_extend_handler(message: types.Message):
    text = '''ℹ️Узнать о приложении больше

Для того чтобы узнать что о проекте пишут в сети пройдите по следующим ссылкам
'''
    builder = InlineKeyboardBuilder()
    builder.adjust(2)
    link_keys = ['about_lenta_ru_01', 'about_iteco_inno_ru_01']
    for key in link_keys:
        # id, url_key, url, "label"
        link_fdb: DictRow = db.ui_links_get_by_key(key)
        target_text = link_fdb.get('label')
        target_link = link_fdb.get('url')
        button = types.InlineKeyboardButton(text=target_text, url=target_link)
        builder.row(button)
    await message.answer(text, reply_markup=builder.as_markup())


@router.message(F.chat.type == 'private', F.text == '🛠 Разработка')
async def develop_page_handler(message: types.Message):
    text = '🛠 Разработка\n'
    text += 'Тут можно получить информацию и ссылки по текущей разработке'
    await message.answer(text, reply_markup=get_develop_buttons())


@router.message(F.chat.type == 'private', F.text == '📝 GitHub')
async def github_page_handler(message: types.Message):
    text = '📝 GitHub\n'
    text += 'Тут можно получить информацию по проекту и ссылки к репозиториям'
    builder = InlineKeyboardBuilder()
    # id, url_key, url, "label"
    link_g: DictRow = db.ui_links_get_by_key('github_main_link')
    g_button = types.InlineKeyboardButton(text=link_g.get('label'), url=link_g.get('url'))
    builder.row(g_button)
    link_gf: DictRow = db.ui_links_get_by_key('github_frontend_link')
    mw_button = types.InlineKeyboardButton(text='🌐 Web', callback_data=CallbackPage(action='front').pack())
    gw_button = types.InlineKeyboardButton(text=link_gf.get('label'), url=link_gf.get('url'))
    builder.row(mw_button, gw_button)
    link_gb: DictRow = db.ui_links_get_by_key('github_backend_link')
    mb_button = types.InlineKeyboardButton(text='🔙🔚 Backend', callback_data=CallbackPage(action='back').pack())
    gb_button = types.InlineKeyboardButton(text=link_gb.get('label'), url=link_gb.get('url'))
    builder.row(mb_button, gb_button)
    link_gi: DictRow = db.ui_links_get_by_key('github_ios_link')
    mi_button = types.InlineKeyboardButton(text='📱 ios разработка', callback_data=CallbackPage(action='ios').pack())
    gi_button = types.InlineKeyboardButton(text=link_gi.get('label'), url=link_gi.get('url'))
    builder.row(mi_button, gi_button)
    link_ga: DictRow = db.ui_links_get_by_key('github_android_link')
    ma_button = types.InlineKeyboardButton(text='📱 android разработка', callback_data=CallbackPage(action='android').pack())
    ga_button = types.InlineKeyboardButton(text=link_ga.get('label'), url=link_ga.get('url'))
    builder.row(ma_button, ga_button)
    mm_button = types.InlineKeyboardButton(text='🏚 На главную', callback_data=CallbackPage(action='main').pack())
    builder.row(mm_button)
    await message.answer(text, reply_markup=builder.as_markup())


@router.message(F.chat.type == 'private', F.text == '🔐 Учетка для тестового приложения')
async def test_app_cred_page_handler(message: types.Message):
    text = '🔐 Учетка для тестового приложения\n'
    text += 'Для получения УЗ для тестового приложения'
    text += 'нажмите на кнопку'
    builder = InlineKeyboardBuilder()
    # id, url_key, url, "label"
    link_cred: DictRow = db.ui_links_get_by_key('test_app_credentials_request')
    button = types.InlineKeyboardButton(text=link_cred.get('label'),
                                        callback_data=CallbackPage(action='get_test_cred').pack())
    builder.row(button)
    await message.answer(text, reply_markup=builder.as_markup())


@router.callback_query(CallbackPage.filter(F.action == 'front'))
async def web_dev_page_callback(call: types.CallbackQuery):
    await call.answer('🌐 Web')
    await web_dev_page_handler(call.message)


@router.message(F.chat.type == 'private', F.text == '🌐 Web')
async def web_dev_page_handler(message: types.Message):
    text = '🌐 Web\n\n'
    text += 'Тут можно получить информацию и запросить доступы'
    text += 'к фронтэнд разработкам'
    builder = InlineKeyboardBuilder()
    # id, url_key, url, "label"
    link_f: DictRow = db.ui_links_get_by_key('figma_web_link')
    builder.button(text=link_f.get('label'), url=link_f.get('url'))
    link_t: DictRow = db.ui_links_get_by_key('trello_frontend_link')
    builder.button(text=link_t.get('label'), url=link_t.get('url'))
    link_c: DictRow = db.ui_links_get_by_key('chat_frontend')
    builder.button(text=link_c.get('label'), url=link_c.get('url'))
    link_g: DictRow = db.ui_links_get_by_key('github_frontend_link')
    builder.button(text=link_g.get('label'), url=link_g.get('url'))
    link_a: DictRow = db.ui_links_get_by_key('frontend_access_link')
    builder.button(text=link_a.get('label'), url=link_a.get('url'))
    builder.adjust(1)

    builder = InlineKeyboardBuilder()
    builder.adjust(2)
    link_keys = ['figma_web_link', 'trello_frontend_link', 'chat_frontend', 'github_frontend_link',
                 'frontend_access_link', 'frontend_system_requirements_link', 'prod_map_miro_link']
    for key in link_keys:
        # id, url_key, url, "label"
        link_fdb: DictRow = db.ui_links_get_by_key(key)
        target_text = link_fdb.get('label')
        target_link = link_fdb.get('url')
        button = types.InlineKeyboardButton(text=target_text, url=target_link)
        builder.row(button)

    await message.answer(text, reply_markup=builder.as_markup())


@router.callback_query(CallbackPage.filter(F.action == 'back'))
async def backend_page_callback(call: types.CallbackQuery):
    await call.answer('🔙🔚 Backend')
    await backend_page_handler(call.message)


@router.message(F.chat.type == 'private', F.text == '🔙🔚 Backend')
async def backend_page_handler(message: types.Message):
    text = '🔙🔚 Backend\n\n'
    text += 'Тут можно получить информацию и запросить доступы'
    text += 'к backend разработке'
    builder = InlineKeyboardBuilder()
    # id, url_key, url, "label"
    builder = InlineKeyboardBuilder()
    builder.adjust(1)
    link_keys = ['figma_backend_link', 'trello_backend_link', 'chat_backend', 'github_backend_link',
                 'backend_knowledge_base_link', 'prod_map_miro_link', 'backend_access_link',
                 'swagger_link', 'test_web_app_link', 'app_prod_link']
    for key in link_keys:
        # id, url_key, url, "label"
        link_fdb: DictRow = db.ui_links_get_by_key(key)
        target_text = link_fdb.get('label')
        target_link = link_fdb.get('url')
        button = types.InlineKeyboardButton(text=target_text, url=target_link)
        builder.row(button)
    cred_fdb: DictRow = db.ui_links_get_by_key('test_app_credentials_request')
    button_cred = types.InlineKeyboardButton(text=cred_fdb.get('label'),
                                             callback_data=CallbackPage(action='get_test_cred').pack())
    builder.row(button_cred)
    await message.answer(text, reply_markup=builder.as_markup())


@router.callback_query(CallbackPage.filter(F.action == 'get_test_cred'))
async def ios_page_callback(call: types.CallbackQuery):
    cred_fdb: DictRow = db.ui_links_get_by_key('test_app_credentials_request')
    cred = cred_fdb.get('url')
    await call.answer(cred, show_alert=True)
    # await ios_dev_page_handler(call.message)


@router.callback_query(CallbackPage.filter(F.action == 'ios'))
async def ios_page_callback(call: types.CallbackQuery):
    await call.answer('📱 ios разработка')
    await ios_dev_page_handler(call.message)


@router.message(F.chat.type == 'private', F.text == '📱 ios разработка')
async def ios_dev_page_handler(message: types.Message):
    text = '📱 ios разработка\n\n'
    text += 'Тут можно получить информацию и запросить доступы'
    text += 'к ios разработкам'

    builder = InlineKeyboardBuilder()
    builder.adjust(1)
    link_keys = ['figma_ios_link', 'trello_ios_link', 'chat_ios', 'github_ios_link',
                 'ios_knowledge_base_link', 'prod_map_miro_link', 'ios_access_link',
                 'swagger_link', 'ios_knowledge_base_link', 'ios_knowledge_base_link']
    for key in link_keys:
        # id, url_key, url, "label"
        link_fdb: DictRow = db.ui_links_get_by_key(key)
        target_text = link_fdb.get('label')
        target_link = link_fdb.get('url')
        button = types.InlineKeyboardButton(text=target_text, url=target_link)
        builder.row(button)

    await message.answer(text, reply_markup=builder.as_markup())


@router.callback_query(CallbackPage.filter(F.action == 'android'))
async def android_page_callback(call: types.CallbackQuery):
    await call.answer('📱 android разработка')
    await android_dev_page_handler(call.message)


@router.message(F.chat.type == 'private', F.text == '📱 android разработка')
async def android_dev_page_handler(message: types.Message):
    text = '📱 android разработка\n\n'
    text += 'Тут можно получить информацию и запросить доступы'
    text += 'к разработкам на андроид'
    builder = InlineKeyboardBuilder()
    builder.adjust(1)
    link_keys = ['chat_android', 'trello_android_link', 'github_android_link', 'figma_android_link',
                 'android_knowledge_base_link', 'prod_map_miro_link', 'android_access_link',
                 'swagger_link']
    for key in link_keys:
        # id, url_key, url, "label"
        link_fdb: DictRow = db.ui_links_get_by_key(key)
        target_text = link_fdb.get('label')
        target_link = link_fdb.get('url')
        button = types.InlineKeyboardButton(text=target_text, url=target_link)
        builder.row(button)
    await message.answer(text, reply_markup=builder.as_markup())


@router.message(F.chat.type == 'private', F.text == '🧑‍💻 Swagger Test')
async def swagger_page_handler(message: types.Message):
    text = '🧑‍💻 Swagger Test\n\n'
    text += 'Для работы со swagger перейдите по ссылке'
    builder = InlineKeyboardBuilder()
    # id, url_key, url, "label"
    link_a: DictRow = db.ui_links_get_by_key('swagger_link')
    builder.button(text=link_a.get('label'), url=link_a.get('url'))
    builder.adjust(1)
    await message.answer(text, reply_markup=builder.as_markup())

