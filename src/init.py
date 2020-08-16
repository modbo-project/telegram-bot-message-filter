import logging

from telegram.ext import MessageHandler, Filters

from telegram import MessageEntity

from modules.pytg.ModulesLoader import ModulesLoader

from .handlers.messages.blacklist import blacklist_message_handler
from .handlers.messages.links_block import links_block_message_handler

def load_message_handlers(dispatcher):
    module_id = ModulesLoader.get_module_id("message_filter")

    dispatcher.add_handler(MessageHandler(Filters.text, blacklist_message_handler), group=module_id)
    dispatcher.add_handler(MessageHandler(Filters.text & (Filters.entity(MessageEntity.URL) | Filters.entity(MessageEntity.TEXT_LINK)), links_block_message_handler), group=module_id + 1)

def initialize():
    logging.info("Initializing message filter module...")

def connect():
    bot_manager = ModulesLoader.load_manager("bot")

    dispatcher = bot_manager.updater.dispatcher

    load_message_handlers(dispatcher)

def load_manager():
    return None

def depends_on():
    return ["config", "tags"]