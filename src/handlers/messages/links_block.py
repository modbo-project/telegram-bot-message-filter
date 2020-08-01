import logging

from modules.pytg.ModulesLoader import ModulesLoader

logger = logging.getLogger(__name__)

def links_block_message_handler(update, context):
    bot = context.bot

    message = update.message

    chat_id = message.chat.id

    config_manager = ModulesLoader.load_manager("config")
    settings = config_manager.load_settings_file("message_filter", "links_block")

    if not settings["block_links"]:
        return

    logger.info("Deleting message with link")

    bot.deleteMessage(
        chat_id = chat_id,
        message_id = message.message_id
    )