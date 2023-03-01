from waifu import Waifu

# Start command
async def start(update, context):
    user_id = update.effective_user.id
    await context.bot.send_message(chat_id=user_id, text="Hi! I'm a waifu catcher bot. Use /help to see the available commands.")

# Help command
async def help(update, context):
    user_id = update.effective_user.id
    help_text = "Available commands:\n\n"
    help_text += "/start - Start the bot\n"
    help_text += "/help - Show this help message\n"
    help_text += "/waifu waifu_name - Catch a waifu by name\n"
    help_text += "/randi waifu_name - Protect a waifu by name\n"
    help_text += "/mywaifus - Show the list of waifus you have caught\n"
    await context.bot.send_message(chat_id=user_id, text=help_text)

# Waifu command
async def catch_waifu(update, context):
    # Get the user ID and waifu name from the command arguments
    user_id = update.effective_user.id
    waifu_name = ' '.join(context.args).capitalize()

    # Catch the waifu if it is available
    await Waifu.catch_waifu(update, context, waifu_name, user_id)

# Randi command
async def protect_waifu(update, context):
    # Get the user ID and waifu name from the command arguments
    user_id = update.effective_user.id
    waifu_name = ' '.join(context.args).capitalize()

    # Protect the waifu if it is available
    await Waifu.protect_waifu(update, context, waifu_name, user_id)

# Mywaifus command
async def list_waifus(update, context):
    # Get the user ID from the update
    user_id = update.effective_user.id

    # Get the list of caught waifus for this user
    caught_waifus = await Waifu.get_caught_waifus(update, context, user_id)

    # Send the list of caught waifus to the user
    if caught_waifus:
        waifus_text = '\n'.join(caught_waifus)
        await context.bot.send_message(chat_id=user_id, text=f"You have caught the following waifus:\n{waifus_text}")
    else:
        await context.bot.send_message(chat_id=user_id, text="You haven't caught any waifus yet.")
