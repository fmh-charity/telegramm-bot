from aiogram.dispatcher.filters.callback_data import CallbackData


class CallbackPage(CallbackData, prefix="page"):
    action: str


class CallbackAdminSetLink(CallbackData, prefix="set_link"):
    action: str
    url_id: int


class CallbackAdminSetForm(CallbackData, prefix="set_form"):
    action: str
    form_id: int
