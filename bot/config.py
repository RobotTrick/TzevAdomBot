from pyrogram import Client, filters
from pyrogram.types import *
from utils import User, commit, Msg, Area, db_session
from json import load

areas = load(open("areas.json", "r", encoding="UTF-8"))

@Client.on_message(filters.command("start"))
def start(_, msg: Message):

    msg.reply("hello!")


@Client.on_message(filters.command("add"))
def add(_, msg: Message):
    uid = msg.from_user.id

    if msg.command == 1:
        msg.reply(Msg.bad_param)
        return

    area_com = " ".join(msg.command[1:])
    if not area_com in areas:
        msg.reply(Msg.area_not_found)
        return

    with db_session:
        area_obj = Area.get(name=area_com)
        if not Area.get(name=area_com):
            area_obj = Area(name=area_com)
            commit()

        user_obj = User.get(uid=uid)
        if not user_obj:
            user_obj = User(uid=uid, area1=area_obj)
            commit()

    msg.reply(Msg.success_config.format(area_com))




