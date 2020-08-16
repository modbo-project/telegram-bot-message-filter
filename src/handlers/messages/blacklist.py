import logging

from modules.pytg.ModulesLoader import ModulesLoader

logger = logging.getLogger(__name__)

def blacklist_message_handler(update, context):
    bot = context.bot

    message = update.message

    chat_id = message.chat.id

    user_id = message.from_user.id
    username = message.from_user.username

    text = message.text

    tags_manager = ModulesLoader.load_manager("tags")
    
    if username:
        if tags_manager.has_tag(username, "no_words_filter", "users"):
            return

    config_manager = ModulesLoader.load_manager("config")
    blacklist_settings = config_manager.load_settings_file("message_filter", "blacklist")

    text_lower = text.lower()

    for kickable_word in blacklist_settings["kickable_words"]:
        if kickable_word in text_lower:
            logger.info("Deleting message '{}' from chat {} as it contains the kickable word '{}'".format(text, chat_id, kickable_word))

            bot.deleteMessage(
                chat_id = chat_id,
                message_id = message.message_id
            )

    bannable_words = 0

    for bannable_word in blacklist_settings["bannable_words"]:
        if bannable_word in text_lower:
            bannable_words += 1

            if bannable_words == 3:
                logger.info("Deleting message '{}' from chat {} and kicking its author as it contains enough bannable words".format(text, chat_id))

                bot.deleteMessage(
                    chat_id = chat_id,
                    message_id = message.message_id
                )

                bot.kickChatMember(
                    chat_id = chat_id,
                    user_id = user_id
                )