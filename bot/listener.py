from pyrogram import Client
from utils import Msg, Area, db_session

app = Client("_alaramSession")


def _send(uid: int, area=None, time=None):
    with app:
        try:
            app.send_message(
                uid,
                Msg.alarms.format(area, time, Msg.info_url)
            )  # שליחת התראה למשתמש
        except:
            pass


def handler(list_alerts):
    for alert in list_alerts:
        area = alert["name"]
        with db_session:
            area_obj = Area.get(name=area)  # קבלת האובייקט מהמסד נתונים
            if area_obj:
                for user in area_obj.get_users():  # לולאה על המנויים לאזור זה
                    _send(user.uid, area, alert["time"])  # שליחת ההתראה
