from pyrogram import Client, filters, types
from utils import *
from json import dump

ids = []


@Client.on_message(filters.command("get_static") & filters.chat(ids))
def get_static(_, msg: types.Message):
    with db_session:
        users = select(user for user in User)[:]
        users_list = [user.uid for user in users]
        with open("users.json", "w") as users_file:
            dump(users_list, users_file, indent=4)

        msg.reply_document("users.json", caption=f"len of users: {len(users_list)}")
