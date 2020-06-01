# -*- coding: UTF-8 -*-
__author__ = 'bespontoff'

import requests
import telebot
from telebot import apihelper

token = '237625759:AAFAgX-oY_lelc1X27PYRZFw0dCykfdR_Qk'
proxies = {
    # 'http': 'http://163.172.182.180:1234',
    'https': 'https://163.172.182.180:1234',
}


class JokeBot:
    about_text = 'JokeBot v.0.1'

    def __init__(self, proxy=None, log_level='INFO'):
        self.bot = telebot.TeleBot(token)
        self.logger = telebot.logger
        telebot.logger.setLevel(log_level)
        if proxy:
            apihelper.proxy = proxy

        self.themes = {
            1: 'Анекдоты',
            2: 'Рассказы',
            3: 'Стишки',
            4: 'Афоризмы',
            5: 'Цитаты',
            6: 'Тосты',
            8: 'Статусы',
            11: 'Анекдоты (+18)',
            12: 'Рассказы (+18)',
            13: 'Стишки (+18)',
            14: 'Афоризмы (+18)',
            15: 'Цитаты (+18)',
            16: 'Тосты (+18)',
            18: 'Статусы (+18)',
        }

    def setup_handlers(self):
        self.logger.info('Setup handlers for bot')
        # тут логика обработчиков

        @self.bot.message_handler(commands=['start', 'help'])
        def handle_start_help(message):
            buttons = self.themes.values()
            markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
            for button in buttons:
                markup.row(button)
            self.bot.send_message(message.chat.id, JokeBot.about_text, reply_markup=markup)

        self.logger.info('Setup handlers complete')

    def run(self, *args, **kwargs):
        self.setup_handlers()
        self.bot.polling(*args, **kwargs)

    def get_fun_content(self, theme: int) -> str:
        """
        :param theme: число от 1 до 18 соответсвующее теме из списка ниже
        :return: str

        Для получения данных в формате json используется запрос: http://rzhunemogu.ru/RandJSON.aspx?CType=?
        где необходимо передать однин из следующих параметров (CType=?):
        1 - Анекдот;
        2 - Рассказы;
        3 - Стишки;
        4 - Афоризмы;
        5 - Цитаты;
        6 - Тосты;
        8 - Статусы;
        11 - Анекдот (+18);
        12 - Рассказы (+18);
        13 - Стишки (+18);
        14 - Афоризмы (+18);
        15 - Цитаты (+18);
        16 - Тосты (+18);
        18 - Статусы (+18);
        """
        api_url = f'http://rzhunemogu.ru/RandJSON.aspx?CType={theme}'
        content = requests.get(api_url).content.decode('windows-1251')
        self.logger.debug(content)
        content = content[12:-2]
        # TODO: сделать 10 и 20 тему, это видео, нужно выдергивать ссылку на видео и отправлять в чат как видео
        return content


if __name__ == '__main__':
    jb = JokeBot(proxy=proxies, log_level='DEBUG')
    # jb.bot.get_me()
    jb.run()
    # joke = jb.get_fun_content(11)
    # print(joke)
