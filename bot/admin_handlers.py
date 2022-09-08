import logging
from logging.config import fileConfig

from aiogram import Router, F, types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from psycopg2.extras import DictRow

from bot import postgre_db
from bot.h_cb_data import CallbackAdminSetLink, CallbackAdminSetForm
from bot.h_fsm import EditLink, CreateLink

fileConfig('logging.ini', disable_existing_loggers=False)
log = logging.getLogger(__name__)
router = Router()
db = postgre_db.Singleton()


@router.message(F.chat.type == 'private', Command(commands="set_links"))
# @router.message(F.chat.type == 'private', F.text == '🧑‍🎨 Дизайн')
async def links_edit_admin_handler(message: types.Message):
    mc = message.chat
    uid = mc.id
    # id, user_id, main_uid, username, name, squad_id, squad_tag, squad_name
    user: DictRow = db.users_get_by_uid(uid)
    if user.get('access') != 100:
        await message.answer('¯\\_(ツ)_/¯')
        return
    text, builder = get_links_admin_message_data(lmax=0)
    await message.answer(text, reply_markup=builder.as_markup())


def get_links_admin_message_data(lmin=-1, lmax=-1):
    text = 'Выберите ссылку которая вас интересует:\n\n'
    builder = InlineKeyboardBuilder()
    links_fdb = None
    if lmax >= 0:
        links_fdb = db.ui_links_get_next_key_list(lmax)
    else:
        links_fdb = db.ui_links_get_prev_key_list(lmin)
    min_max: DictRow = db.ui_links_get_min_max_id()
    row = []
    length = len(links_fdb)
    first_id = links_fdb[0].get('id')
    last_id = links_fdb[length - 1].get('id')
    if first_id != min_max.get('min'):
        prev_b = types.InlineKeyboardButton(text='Назад',
                                            callback_data=CallbackAdminSetLink(action='prev', url_id=first_id).pack())
        row.append(prev_b)
    cancel_b = types.InlineKeyboardButton(text='Завершить',
                                          callback_data=CallbackAdminSetLink(action='finish', url_id=0).pack())
    row.append(cancel_b)
    if last_id != min_max.get('max'):
        next_b = types.InlineKeyboardButton(text='Вперед',
                                            callback_data=CallbackAdminSetLink(action='next', url_id=last_id).pack())
        row.append(next_b)
    builder.row(*row)
    for link_fdb in links_fdb:
        # text += f'/set_ui_link_{link_fdb.get("url_key")}\n'  # TODO: Может реализовать такое
        text += f'{link_fdb.get("url_key")}\n'
        button = InlineKeyboardButton(text=f'{link_fdb.get("url_key")}',
                                      callback_data=CallbackAdminSetLink(action='view',
                                                                         url_id=link_fdb.get("id")).pack())
        builder.row(button)
    builder.row(*row)
    return text, builder


@router.callback_query(CallbackAdminSetLink.filter(F.action == 'finish'))
async def finish_links_admin_callback(call: types.CallbackQuery):
    await call.message.delete_reply_markup()
    await call.answer('Закончили')


@router.callback_query(CallbackAdminSetLink.filter(F.action == 'next'))
async def next_links_admin_callback(call: types.CallbackQuery, callback_data: CallbackAdminSetLink):
    text, builder = get_links_admin_message_data(lmax=callback_data.url_id)
    await call.message.edit_text(f'{text}', reply_markup=builder.as_markup())
    # await call.message.delete_reply_markup()
    await call.answer('Вперед')


@router.callback_query(CallbackAdminSetLink.filter(F.action == 'prev'))
async def prev_links_admin_callback(call: types.CallbackQuery, callback_data: CallbackAdminSetLink):
    text, builder = get_links_admin_message_data(lmin=callback_data.url_id)
    await call.message.edit_text(f'{text}', reply_markup=builder.as_markup())
    # await call.message.delete_reply_markup()
    await call.answer('Назад')


@router.callback_query(CallbackAdminSetLink.filter(F.action == 'view'))
async def view_links_admin_callback(call: types.CallbackQuery, callback_data: CallbackAdminSetLink):
    link: DictRow = db.ui_links_get_by_id(callback_data.url_id)
    text = 'Ссылка:\n\n'
    text += 'Key:\n'
    text += f"{link.get('url_key')}\n"
    text += 'label:\n'
    text += f"{link.get('label')}\n"
    text += 'url:\n'
    text += f"{link.get('url')}\n"

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text='Отменить',
                                           callback_data=CallbackAdminSetLink(action='finish', url_id=0).pack()))
    builder.row(InlineKeyboardButton(text='Изменить метку (label)',
                                     callback_data=CallbackAdminSetLink(action='edit_l',
                                                                        url_id=link.get("id")).pack()))
    builder.row(InlineKeyboardButton(text='Изменить ссылку (url)',
                                     callback_data=CallbackAdminSetLink(action='edit_u',
                                                                        url_id=link.get("id")).pack()))
    await call.message.edit_text(f'{text}', reply_markup=builder.as_markup())
    # await call.message.delete_reply_markup()
    await call.answer('Ок')


@router.callback_query(CallbackAdminSetLink.filter(F.action == 'edit_u'))
async def edit_url_links_admin_callback(call: types.CallbackQuery, callback_data: CallbackAdminSetLink,
                                        state: FSMContext):
    link: DictRow = db.ui_links_get_by_id(callback_data.url_id)
    await state.set_state(EditLink.l_id)
    await state.update_data(l_id=callback_data.url_id)
    await state.set_state(EditLink.url)
    text = '<b>Текущие данные:</b>\n\n'
    text += get_text_4links_admin_edit(link)
    text += '<i>Введите актуальный url:</i>'
    await call.message.edit_text(f'{text}')
    # await call.message.delete_reply_markup()
    await call.answer('...')


@router.message(EditLink.url)
async def edit_url_links_admin_handler(message: types.Message, state: FSMContext):
    url = message.text
    if not url.lower().startswith('https://'):
        if not url.lower().startswith('http://'):
            await state.clear()
            await message.answer('не корректная ссылка.\nДействие отменено.')
            return
    await state.update_data(url=url)
    data = await state.get_data()
    db.ui_links_update_url_by_id(data.get('l_id'), data.get('url'))
    await state.clear()
    link: DictRow = db.ui_links_get_by_id(data.get('l_id'))
    text = '<b>Обновленные данные:</b>\n\n'
    text += get_text_4links_admin_edit(link)
    await message.answer(text=text)


@router.callback_query(CallbackAdminSetLink.filter(F.action == 'edit_l'))
async def edit_label_links_admin_callback(call: types.CallbackQuery, callback_data: CallbackAdminSetLink,
                                          state: FSMContext):
    link: DictRow = db.ui_links_get_by_id(callback_data.url_id)
    await state.set_state(EditLink.l_id)
    await state.update_data(l_id=callback_data.url_id)
    await state.set_state(EditLink.label)
    text = '<b>Текущие данные:</b>\n\n'
    text += get_text_4links_admin_edit(link)
    text += '<i>Введите актуальный url:</i>'
    await call.message.edit_text(f'{text}')
    # await call.message.delete_reply_markup()
    await call.answer('...')


@router.message(EditLink.label)
async def edit_label_links_admin_handler(message: types.Message, state: FSMContext):
    label = message.text
    if label.lower() == 'отмена':
        await state.clear()
        await message.answer('¯\\_(ツ)_/¯\nОперация отменена.')
        return
    await state.update_data(label=label)
    data = await state.get_data()
    db.ui_links_update_label_by_id(data.get('l_id'), data.get('label'))
    await state.clear()
    link: DictRow = db.ui_links_get_by_id(data.get('l_id'))
    text = '<b>Обновленные данные:</b>\n\n'
    text += get_text_4links_admin_edit(link)
    await message.answer(text=text)


def get_text_4links_admin_edit(link: DictRow):
    text = '<i>Key:</i>\n'
    text += f"{link.get('url_key')}\n\n"
    text += '<i>label:</i>\n'
    text += f"{link.get('label')}\n\n"
    text += '<i>url:</i>\n'
    text += f"{link.get('url')}\n\n"
    return text


@router.message(F.chat.type == 'private', Command(commands="add_link"))
# @router.message(F.chat.type == 'private', F.text == '🧑‍🎨 Дизайн')
async def links_create_admin_handler(message: types.Message, state: FSMContext):
    mc = message.chat
    uid = mc.id
    # id, user_id, main_uid, username, name, squad_id, squad_tag, squad_name
    user: DictRow = db.users_get_by_uid(uid)
    if user.get('access') != 100:
        await message.answer('¯\\_(ツ)_/¯')
        return

    await state.set_state(CreateLink.key)
    text = 'Введите ключ ссылки\nВведите "Отмена" чтобы прервать операцию'
    await message.answer(text)


@router.message(CreateLink.key)
async def edit_label_links_admin_handler(message: types.Message, state: FSMContext):
    key = message.text
    if key.lower() == 'отмена':
        await state.clear()
        await message.answer('¯\\_(ツ)_/¯\nОперация отменена.')
        return
    await state.update_data(key=key)
    await state.set_state(CreateLink.url)
    await message.answer('Введите ссылку (url)')


@router.message(CreateLink.url)
async def edit_label_links_admin_handler(message: types.Message, state: FSMContext):
    url = message.text
    if url.lower() == 'отмена':
        await state.clear()
        await message.answer('¯\\_(ツ)_/¯\nОперация отменена.')
        return
    elif not url.lower().startswith('https://'):
        if not url.lower().startswith('http://'):
            await state.clear()
            await message.answer('не корректная ссылка.\nДействие отменено.')
            return
    await state.update_data(url=url)
    await state.set_state(CreateLink.label)
    await message.answer('Введите текст ссылки (label)')


@router.message(CreateLink.label)
async def edit_label_links_admin_handler(message: types.Message, state: FSMContext):
    label = message.text
    if label.lower() == 'отмена':
        await state.clear()
        await message.answer('¯\\_(ツ)_/¯\nОперация отменена.')
        return
    await state.update_data(label=label)
    data = await state.get_data()
    db.ui_links_add_new_link(data.get('key'), data.get('url'), data.get('label'))
    await state.clear()
    text = '<b>Ссылка добавлена</b>\n\n'
    await message.answer(text=text)


def get_form_admin_message_data(lmin=-1, lmax=-1):
    text = 'Выберите форму которая вас интересует:\n\n'
    builder = InlineKeyboardBuilder()
    forms = None
    if lmax >= 0:
        forms = db.ui_form_get_next_key_list(lmax)
    else:
        forms = db.ui_form_get_prev_key_list(lmin)
    min_max: DictRow = db.ui_form_get_min_max_id()
    row = []
    length = len(forms)
    first_id = forms[0].get('id')
    last_id = forms[length - 1].get('id')
    if first_id != min_max.get('min'):
        prev_b = types.InlineKeyboardButton(text='Назад',
                                            callback_data=CallbackAdminSetForm(action='prev', form_id=first_id).pack())
        row.append(prev_b)
    cancel_b = types.InlineKeyboardButton(text='Завершить',
                                          callback_data=CallbackAdminSetForm(action='finish', form_id=0).pack())
    row.append(cancel_b)
    if last_id != min_max.get('max'):
        next_b = types.InlineKeyboardButton(text='Вперед',
                                            callback_data=CallbackAdminSetForm(action='next', url_id=last_id).pack())
        row.append(next_b)
    builder.row(*row)
    for form in forms:
        # text += f'/set_ui_link_{link_fdb.get("url_key")}\n'  # TODO: Может реализовать такое
        text += f'{form.get("url_key")} ({form.get("sequence")})\n'
        button = InlineKeyboardButton(text=f'{form.get("url_key")}',
                                      callback_data=CallbackAdminSetForm(action='view',
                                                                         url_id=form.get("id")).pack())
        builder.row(button)
    builder.row(*row)
    return text, builder


@router.message(F.chat.type == 'private', Command(commands="set_ui_form"))
async def ui_form_edit_handler(message: types.Message):
    mc = message.chat
    uid = mc.id
    # id, user_id, main_uid, username, name, squad_id, squad_tag, squad_name
    user: DictRow = db.users_get_by_uid(uid)
    if user.get('access') != 100:
        await message.answer('¯\\_(ツ)_/¯')
        return
    text, builder = get_form_admin_message_data(lmax=0)
    await message.answer(text, reply_markup=builder.as_markup())