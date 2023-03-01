from pyrogram.types import Message
from randikhana import Randikhana
from randi import Randi

def handle_start_command(client: 'Client', message: Message):
    """
    Handle the /start command.
    """
    client.send_message(
        chat_id=message.chat.id,
        text="Hi! I'm a waifu catcher bot. Send me /waifu command to get a random waifu."
    )

def handle_waifu_command(client: 'Client', message: Message):
    """
    Handle the /waifu command.
    """
    # delete the previous waifu's message
    prev_waifu = Database.get_current_waifu(message.chat.id)
    if prev_waifu:
        client.delete_messages(chat_id=message.chat.id, message_ids=prev_waifu["message_id"])

    # send a new waifu message
    waifu = Randi.get_random_waifu()
    message = client.send_photo(chat_id=message.chat.id, photo=waifu["pic"], caption=waifu["name"])
    Database.save_waifu(chat_id=message.chat.id, waifu=waifu, message_id=message.message_id)

def handle_randi_command(client: 'Client', message: Message):
    """
    Handle the /randi command.
    """
    # get the waifu name from the command
    waifu_name = message.text.split(maxsplit=1)[1].strip()

    # get the current waifu and its chat ID
    current_waifu = Database.get_current_waifu(message.chat.id)
    if not current_waifu:
        client.send_message(chat_id=message.chat.id, text="No waifu currently available.")
        return
    chat_id = current_waifu["chat_id"]

    # check if the waifu name matches
    if waifu_name.lower() == current_waifu["waifu"]["name"].lower():
        client.send_message(chat_id=message.chat.id, text="You have protected the waifu!")
        Database.add_user(chat_id=chat_id, user_id=message.from_user.id)
    else:
        client.send_message(chat_id=message.chat.id, text="Wrong waifu name!")

def handle_myrandi_command(client: 'Client', message: Message):
    """
    Handle the /myrandi command.
    """
    chat_id = message.chat.id
    users = Database.get_users(chat_id)

    if not users:
        client.send_message(chat_id=chat_id, text="No users have protected the waifu yet.")
        return

    user_list = "\n".join([f"{u['first_name']} ({u['id']})" for u in users])
    client.send_message(chat_id=chat_id, text=f"Users who have protected the waifu:\n{user_list}")
