import logging

from modules.pytg.ModulesLoader import ModulesLoader

logger = logging.getLogger(__name__)

def blacklist_message_handler(update, context):
    bot = context.bot

    message = update.message

    chat_id = message.chat.id

    text = message.text

    config_manager = ModulesLoader.load_manager("config")
    blacklist_settings = config_manager.load_settings_file("message_filter", "blacklist")

    for forbidden_word in blacklist_settings["forbidden_words"]:
        if forbidden_word in text:
            logger.info("Deleting message '{}' from chat {} as it contains the forbidden word '{}'".format(text, chat_id, forbidden_word))

            bot.deleteMessage(
                chat_id = chat_id,
                message_id = message.message_id
            )