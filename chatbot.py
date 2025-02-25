import telegram
from telegram.ext import Updater, MessageHandler, Filters
import configparser
import logging

def main():
    # 加载配置文件
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    # 创建更新器
    updater = Updater(
        token=config["TELEGRAM"]["ACCESS_TOKEN"],
        use_context=True
    )
    dispatcher = updater.dispatcher

    # 配置日志
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    # 注册消息处理器
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    # 启动机器人
    updater.start_polling()
    updater.idle()

def echo(update, context):
    """回显用户消息"""
    reply_message = update.message.text.upper()
    logging.info(f"Update: {update}")
    logging.info(f"Context: {context}")
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply_message
    )

if __name__ == '__main__':
    main()