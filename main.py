# בוט צבע אדום לשליחת התראות על אזעקת צבע אדום לפי מיקום.
# נוצר ע"י Yeuda-By ודוד לב, בעזרת ספריית צבע אדום (https://www.tzevaadom.co.il/)
# שימו לב: אין לסמוך על הבוט במקרה של סכנת חיי אדם, וחובה לפעול על פי הוראות פיקוד העורף.

from pyrogram import Client
from tzevaadom import tzevaadom

from bot.listener import handler

if __name__ == '__main__':
    app = Client("TzevAdom", plugins=dict(root="bot"))
    tzevaadom.alerts_listener(handler)  # הרצת ה"האזנה לאזעקות"
    app.run()  # הרצת הבוט
