import logging

from modules.pytg.ModulesLoader import ModulesLoader

logger = logging.getLogger(__name__)

def links_block_message_handler(update, context):
    bot = context.bot

    message = update.message

    chat_id = message.chat.id

    username = message.from_user.username

    config_manager = ModulesLoader.load_manager("config")
    settings = config_manager.load_settings_file("message_filter", "links_block")

    if not settings["block_links"]:
        return

    chat_admins = message.chat.get_administrators()

    if settings["admins_authorized"]:
        for chat_admin in chat_admins:
            if message.from_user.id == chat_admin.user.id:
                logging.info("User is an administrator of the chat")
                return

    logger.info("Detected message with link")

    tags_manager = ModulesLoader.load_manager("tags")
    
    if username:
        if tags_manager.has_tag(username, "can_post_links", "users"):
            logger.info("User is allowed to post links")
            return

    logger.info("Deleting message with link")

    bot.deleteMessage(
        chat_id = chat_id,
        message_id = message.message_id
    )