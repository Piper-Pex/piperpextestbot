#docker run --name chatbot  -d --env TELEGRAM_ACCESS_TOKEN=7887521281:AAHDyoUpCmCjkMoXB4Xh53TZYODxQuUQvwE  --env CHATGPT_ACCESS_TOKEN=ae68d010-92d4-4730-af02-84a20f05b7d1    --env CHATGPT_MODEL_NAME=gpt-4-o-mini            piperpextestbotcontainer:v1     python botchatbot.py 664b158bfab048956367f0600b06fe287b7a9267c1f86c6def9b5e2d25fe31b9

from telegram import Update
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, CallbackContext)
import configparser
import logging
import redis
from ChatGPT_HKBU import HKBU_ChatGPT

global redis1

def main():
    # Load your token and create an Updater for your Bot
    config = configparser.ConfigParser()
    config.read('config.ini')
    updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher

    global redis1
    redis1 = redis.Redis(
        host=(config['REDIS']['HOST']),
        password=(config['REDIS']['PASSWORD']),
        port=(config['REDIS']['REDISPORT']),
        decode_responses=(config['REDIS']['DECODE_RESPONSE']),
        username=(config['REDIS']['USER_NAME'])
    )

    # Logging setup
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    # Register command handlers
    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("hello", hello_command))
    dispatcher.add_handler(CommandHandler("set_interest", set_interest))
    dispatcher.add_handler(CommandHandler("match", match_users))

    # Register ChatGPT handler
    global chatgpt
    chatgpt = HKBU_ChatGPT(config)
    chatgpt_handler = MessageHandler(Filters.text & (~Filters.command), equiped_chatgpt)
    dispatcher.add_handler(chatgpt_handler)

    # Start the bot
    updater.start_polling()
    updater.idle()

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Helping you helping you.')

def add(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /add is issued."""
    try:
        global redis1
        logging.info(context.args[0])
        msg = context.args[0]  # /add keyword
        redis1.incr(msg)
        update.message.reply_text(f'You have said {msg} for {redis1.get(msg)} times.')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /add <keyword>')

def hello_command(update: Update, context: CallbackContext) -> None:
    """Send greeting when /hello is issued"""
    try:
        name = context.args[0]
        update.message.reply_text(f'Good day, {name}!')
    except IndexError:
        update.message.reply_text('Usage: /hello <name>')

def equiped_chatgpt(update, context):
    """Handle ChatGPT responses."""
    global chatgpt
    reply_message = chatgpt.submit(update.message.text)
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)

def set_interest(update: Update, context: CallbackContext) -> None:
    """Set user's interest."""
    try:
        user_id = update.message.from_user.id
        username = update.message.from_user.username
        interest = context.args[0]  # /set_interest <interest>

        # Store user info in Redis
        redis1.hset(f"user:{user_id}", mapping={
            "username": username,
            "interest": interest
        })
        update.message.reply_text(f"Your interest '{interest}' has been recorded!")
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set_interest <interest>')

def match_users(update: Update, context: CallbackContext) -> None:
    """Match users with similar interests."""
    user_id = update.message.from_user.id
    user_data = redis1.hgetall(f"user:{user_id}")

    if not user_data:
        update.message.reply_text("You haven't set your interest yet! Use /set_interest <interest>.")
        return

    user_interest = user_data["interest"]
    matched_users = []

    # Scan all users in Redis
    for key in redis1.keys("user:*"):
        if key != f"user:{user_id}":  # Skip self
            data = redis1.hgetall(key)
            if data["interest"] == user_interest:
                matched_users.append(data["username"])

    if matched_users:
        update.message.reply_text(f"Users with similar interest '{user_interest}': {', '.join(matched_users)}")
    else:
        update.message.reply_text(f"No users found with similar interest '{user_interest}'.")

if __name__ == '__main__':
    main()