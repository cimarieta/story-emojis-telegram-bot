"""
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import click
from telegram.ext import Updater, CommandHandler
import telegram.parsemode
import logging

from random_emoji import random_emoji

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update, chat_data):
    chat_data['n'] = 7
    #update.message.reply_text('Hi! Use /set <n> to set the number of emojis (default is n=7)')
    with open('help.md', 'r') as f:
        help_txt = f.read()
    update.message.reply_text(help_txt, parse_mode=telegram.parsemode.ParseMode.MARKDOWN)


def display_emoji(bot, update, chat_data):
    emojis = [random_emoji()[0] for i in range(chat_data['n'])]
    update.message.reply_text(''.join(emojis))


def set_number_emojis(bot, update, args, chat_data):
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        n = int(args[0])
        if n < 1 or n > 10:
            update.message.reply_text('Escolha `n` de forma que: `1 <= n <= 10`',
                parse_mode=telegram.parsemode.ParseMode.MARKDOWN)
            return

        # Add job to queue
        chat_data['n'] = n

        update.message.reply_text('Ok! As sequências terão {} emojis'.format(chat_data['n']))

    except (IndexError, ValueError):
        update.message.reply_text('Uso correto: /set <número-de-emojis>')


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


@click.command()
@click.option('--token', help='token do seu bot')
def main(token):
    """Run bot."""
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start, pass_chat_data=True))
    dp.add_handler(CommandHandler("help", start))
    dp.add_handler(CommandHandler("set", set_number_emojis,
                                  pass_args=True,
                                  pass_job_queue=False,
                                  pass_chat_data=True))
    dp.add_handler(CommandHandler("emoji", display_emoji,
                                  pass_args=False,
                                  pass_job_queue=False,
                                  pass_chat_data=True))
    #dp.add_handler(CommandHandler("unset", unset, pass_chat_data=True))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
