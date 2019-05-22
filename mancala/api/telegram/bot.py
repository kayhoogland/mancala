from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from telegram import ReplyKeyboardMarkup
import requests
import logging
import os
from dotenv import load_dotenv, find_dotenv
from mancala.game.create import Board, Player
from mancala.game.play import Game

logger = logging.getLogger()
logger.setLevel('INFO')
logger.addHandler(logging.StreamHandler())
load_dotenv(find_dotenv())

game = None

def get_random_dog(bot, update):
    url = requests.get('https://random.dog/woof.json').json()['url']
    logger.debug(f"Getting random dog picture from: f{url}")

    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=url)


def choice(bot, update):
    menu_keyboard = [[str(option) for option in range(1, 7)]]
    menu_markup = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=False, resize_keyboard=True)
    info = bot.send_message(chat_id=update.message.chat_id, text='Choose wisely...', reply_markup=menu_markup)
    logger.info(f'User choose pit nr {info}.')


def start_new_game(bot, update):
    user = update.message.from_user['first_name']
    p1_name, p2_name = user, 'Kay'
    logger.info('Starting new game between {p1_name} & {p2_name}')
    global game
    board = Board(4, p1_name, p2_name)
    game = Game(board)
    bot.send_message(chat_id=update.message.chat_id, text=str(game))


def move(bot, update):
    user = update.message.from_user['first_name']
    action = update.message.text
    try:
        action = int(action)
    except (ValueError, TypeError):
        pass
    if action in range(1,7):
        text = f'{user} has sent me action {action}.'
        logger.info(text)
        bot.send_message(chat_id=update.message.chat_id, text=text)






def main():
    updater = Updater(os.environ.get('TELEGRAM_API_TOKEN'))
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('dog', get_random_dog))
    dp.add_handler(CommandHandler('keyboard', choice))
    dp.add_handler(CommandHandler('start', start_new_game))
    dp.add_handler(MessageHandler(Filters.text, move))

    logger.info('The Telegram bot is live and ready for use')
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
