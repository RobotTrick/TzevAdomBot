from json import load

from pyrogram import filters
from pyrogram.types import *

from bot.listener import *
from utils import User, commit

areas = load(open("areas.json", "r", encoding="UTF-8"))  # קובץ המיקומים
""" הקובץ זמין גם בכתובת: https://m100achuz.ml/areas.html """


@Client.on_message(filters.command("start"))
def start(_, msg: Message):
    uid = msg.from_user.id

    with db_session:
        if not User.get(uid=uid):
            User(uid=uid)  # יצירת אובייקט המשתמש אם לא קיים
            commit()

    msg.reply(Msg.start)  # שליחת הודעת סטארט


@Client.on_message(filters.command("add") & filters.private)
def add(_, msg: Message):
    uid = msg.from_user.id

    if len(msg.command) == 1:
        msg.reply(Msg.bad_param)  # החזרת שגיאה בשליחת פקודה ללא פרמטרים
        return

    area_com = " ".join(msg.command[1:])  # יצירת שם אזור מהפקודה
    if area_com not in areas:
        msg.reply(Msg.area_not_found)  # החזרת שגיאה באזור לא קיים
        return

    with db_session:
        area_obj = Area.get(name=area_com)
        if not Area.get(name=area_com):
            area_obj = Area(name=area_com)
            commit()  # קבלת/יצירת אובייקט אזור

        user_obj = User.get(uid=uid)
        if not user_obj:
            User(uid=uid, area1=area_obj)
            commit()  # יצירת אובייקט משתמש אם לא קיים, והרשמה לאיזור
        else:
            user_obj.area1.add(area_obj)
            commit()  # הרשמה לאזור למשתמש קיים

    msg.reply(Msg.success_config.format(area_obj.name))  # החזרת הודעת "הרשמה הצליחה"


@Client.on_message(filters.command("remove") & filters.private)
def remove(_, msg: Message):
    uid = msg.from_user.id

    if len(msg.command) == 1:
        msg.reply(Msg.bad_param)
        return  # החזרת שגיאה בקבלת פקודה ללא פרמטרים

    area_com = " ".join(msg.command[1:])  # יצירת שם האזור
    with db_session:
        area_obj = Area.get(name=area_com)
        if area_com not in areas or not area_obj:
            msg.reply(Msg.area_not_found)
            return  # החזרת שגיאה באזור לא קיים

        user_obj = User.get(uid=uid)
        if not user_obj:
            msg.reply(Msg.none_subscribes)
            return  # החזרת שגיאה במשתמש ללא מנויים
        subs = [ar.name for ar in user_obj.area1]

        if area_com not in subs:
            msg.reply(Msg.not_subscribe)
            return  # החזרת שגיאה במשתמש לא מנוי לאיזור ספציפי

        user_obj.area1.remove(area_obj)
        commit()  # הסרת המשתמש מהאיזור

    msg.reply(Msg.success_remove)  # החזרת הודעה "הסרת איזור הצליחה"


@Client.on_message(filters.command("list") & filters.private)
def _list(_, msg: Message):
    uid = msg.from_user.id

    with db_session:
        user_obj = User.get(uid=uid)
        if not user_obj:
            msg.reply(Msg.none_subscribes)
            return  # החזרת שגיאה במשתמש ללא רשומים

        subs = [ar.name for ar in user_obj.area1]  # יצירת רשימה של איזורים רשומים

    msg.reply(Msg.list_subscribes(subs))  # החזרת הודעה "רשימת מנויים"


@Client.on_message(filters.command("help"))
def _help(_, msg: Message):
    msg.reply(
        Msg.help,
        # disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
            "💬 קוד המקור של הבוט", url="https://google.com"
        )]])
    )  # החזרת הודעת עזרה
