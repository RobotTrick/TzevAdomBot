from typing import List
from pony.orm import *


# ====== DB ======
db = Database()


class User(db.Entity):
    uid = PrimaryKey(int, auto=True)
    area1 = Required(lambda: Area)
    # area2 = Optional(lambda: Area)


class Area(db.Entity):
    name = Required(str)
    users = Set(lambda: User)

    def get_users(self) -> list:
        ids = []
        print(self.users)
        for user in self.users:
            ids.append(user.uid)
        return ids


db.bind(provider='sqlite', filename='tsevaAdom.sqlite', create_db=True)
db.generate_mapping(create_tables=True)


# ===== API ======

# ===== KEYBOARDS =====

# ==== MSG =====
class Msg:
    bad_param = "לא הוזנו פרמטרים ):"
    _areas_url = "https://m100achuz.ml/areas.html"
    area_not_found = f"לא נמצאה עיר/אזור. תוכלו למצוא את רשימת הערים, [כאן]({_areas_url})"
    success_config = "נרשמת בהצלחה לקבלת התראות צבע אדום לאזור: **{}**. בשורות טובות."