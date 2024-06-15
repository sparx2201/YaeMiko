from typing import List, Optional, Union
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    InlineQueryHandler,
    MessageHandler,
    Application,
)
from telegram.ext.filters import MessageFilter
from Mikobot import LOGGER
from Mikobot import dispatcher as n
from Mikobot.plugins.disable import DisableAbleCommandHandler, DisableAbleMessageHandler

class ExonTelegramHandler:
    def __init__(self, n):
        self._dispatcher = n

    def command(
        self,
        command: str,
        filters: Optional[MessageFilter] = None,
        admin_ok: bool = False,
        can_disable: bool = True,
        group: Optional[Union[int, str]] = 40,
        block: bool = True,
    ):
        def _command(func):
            async def async_func(update, context):
                await func(update, context)

            if can_disable:
                handler = DisableAbleCommandHandler(
                    command,
                    async_func,
                    filters=filters,
                    admin_ok=admin_ok,
                    block=block,
                )
            else:
                handler = CommandHandler(
                    command,
                    async_func,
                    filters=filters,
                    block=block,
                )

            self._dispatcher.add_handler(handler, group)
            LOGGER.debug(
                f"[ExonCMD] Loaded handler {command} for function {func.__name__} in group {group}"
            )
            return func

        return _command

    def message(
        self,
        pattern: Optional[str] = None,
        can_disable: bool = True,
        group: Optional[Union[int, str]] = 60,
        friendly=None,
        block: bool = True,
    ):
        def _message(func):
            async def async_func(update, context):
                await func(update, context)

            if can_disable:
                handler = DisableAbleMessageHandler(
                    pattern, async_func, friendly=friendly, block=block
                )
            else:
                handler = MessageHandler(pattern, async_func, block=block)

            self._dispatcher.add_handler(handler, group)
            LOGGER.debug(
                f"[ExonMSG] Loaded filter pattern {pattern} for function {func.__name__} in group {group}"
            )
            return func

        return _message

    def callbackquery(self, pattern: str = None):
        def _callbackquery(func):
            async def async_func(update, context):
                await func(update, context)

            self._dispatcher.add_handler(
                CallbackQueryHandler(
                    pattern=pattern, callback=async_func
                )
            )
            LOGGER.debug(
                f"[ExonCALLBACK] Loaded callbackquery handler with pattern {pattern} for function {func.__name__}"
            )
            return func

        return _callbackquery

    def inlinequery(
        self,
        pattern: Optional[str] = None,
        chat_types: List[str] = None,
        block: bool = True,
    ):
        def _inlinequery(func):
            async def async_func(update, context):
                await func(update, context)

            self._dispatcher.add_handler(
                InlineQueryHandler(
                    pattern=pattern,
                    callback=async_func,
                    chat_types=chat_types,
                    block=block,
                )
            )
            LOGGER.debug(
                f"[ExonINLINE] Loaded inlinequery handler with pattern {pattern} for function {func.__name__} | CHAT TYPES: {chat_types}"
            )
            return func

        return _inlinequery


Exoncmd = ExonTelegramHandler(n).command
Exonmsg = ExonTelegramHandler(n).message
Exoncallback = ExonTelegramHandler(n).callbackquery
Exoninline = ExonTelegramHandler(n).inlinequery
