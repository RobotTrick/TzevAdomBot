from typing import List

from pony.orm import *


# ====== DB ======
db = Database()

class User(db.Entity):
    uid = PrimaryKey(int, auto=True)
    area = Set("Area")


class Area(db.Entity):
    name = Required(str)
    users = Set(User)

    def get_users(self) -> List[User]:
        return self.users[:]


db.bind(provider='sqlite', filename='tsevaAdom.sqlite', create_db=True)
db.generate_mapping(create_tables=True)


with db_session:
    yuda = User(uid=1236)
    ash = Area(name="ash")
    commit()
    ash.users = yuda
    commit()
    print(ash.get_users())