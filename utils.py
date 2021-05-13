from pony.orm import *

# ====== DB ======
db = Database()


class User(db.Entity):
    uid = PrimaryKey(int, auto=True)
    area1 = Set(lambda: Area)


class Area(db.Entity):
    name = Required(str)
    users = Set(lambda: User)

    def get_users(self) -> list:
        ids = []
        for user in self.users:
            ids.append(user.uid)
        return ids  # החזרת רשימת מנויים לפי אזור


db.bind(provider='sqlite', filename='tsevaAdom.sqlite', create_db=True)
db.generate_mapping(create_tables=True)


# ==== MSG =====
class Msg:
    bad_param = "לא הוזנו פרמטרים ):\nהפורמט הנכון לשימוש בפקודה הוא:\n\n" \
                "```/add שם האזור" \
                "\n/remove שם האזור```"
    _areas_url = "https://m100achuz.ml/areas.html"  # רשימת האזורים
    area_not_found = f"לא נמצאה עיר/אזור. תוכלו למצוא את רשימת הערים [כאן]({_areas_url})."
    success_config = "נרשמת בהצלחה לקבלת התראות צבע אדום לאזור: **{}**. בשורות טובות."
    _info_url = "https://www.oref.org.il/12487-15894-he/Pakar.aspx"  # הוראות פיקוד העורף
    alarms = "🛑 אזעקת צבע אדום כעת באזורך: **{}**. \n\nיש לכם **{}** כדי להגיע למרחב המוגן.\nלעוד מידע הכנסו ל[אתר " \
             "פיקוד העורף]({}). "
    none_subscribes = "נראה שעדיין לא נרשמת לאזור כלשהוא. תוכל להרשם לאזורך על ידי פקודת /add."
    not_subscribe = "אינך רשום לאזור זה."
    success_remove = "אזור זה הוסר מרשימת האזורים שלך."

    help = "להלן הפקודות הנתמכות בבוט:\n\n" \
           "#️⃣ /add:\n" \
           "משתמש להוספת אזור/עיר לרשימת האזורים שלך. השימוש בפקודה מתבצע באמצעות שליחת הפקודה יחד עם שם האזור. " \
           "לדוגמה:\n" \
           "`/add ירושלים - מזרח, מרכז ומערב`\n" \
           f"\nשימו לב שהבוט מקבל אך ורק שמות מדויקים, מתוך הרשימה המופיעה [כאן]({_areas_url}). אנחנו ממליצים להכנס " \
           f"לרשימה, לעשות חיפוש בדף (דרך דפדפן Chrome), ולוודא שיש ברשימה את השם המדויק.\n\n" \
           "#️⃣ /remove:\n" \
           "הסרת אזור מרשימת האזורים שלך. אופן השימוש בפקודה הוא בדומה לפקודת /add:\n" \
           "`/remove ירושלים - מזרח, מרכז ומערב`\n\n" \
           "#️⃣ /list:" \
           "\nרשימת כל האזורים שהנך רשום/ה לקבלת התראות עליהם.\n\n" \
           "בוט זה נוצר על ידי " \
           "[Yeuda-By](t.me/m100achuzBots) && [David Lev](t.me/davidlev) מצוות " \
           "[רובוטריק](https://t.me/RobotTrick)."

    start = "hello"

    def list_subscribes(subs: list) -> str:
        """ החזרת הודעת "רשימת מנויים" על פי ליסט של איזורים """
        _len = len(subs)
        str_subs = "\n".join(subs)
        txt = f"**סך כל האזורים שהנך רשום אליהם: {_len}.**" \
              f"\n```{str_subs}```.\nלהסרת אזור, השתמשו בפקודת /remove."
        return txt

    @property
    def info_url(self):
        return self._info_url
