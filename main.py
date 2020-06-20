# -*- coding: UTF-8 -*-
__author__ = 'bespontoff'

import os
import random

import freeproxy
import requests
import telebot
from freeproxy import from_cn_proxy, from_cyber_syndrome, from_free_proxy_list, from_proxy_spy, from_hide_my_ip
from telebot import apihelper
from urllib3.exceptions import ReadTimeoutError, MaxRetryError


class JokeBot:
    about_text = 'JokeBot v.0.1'

    def __init__(self, proxy=None, log_level='INFO'):
        self.token = os.environ.get('TG_BOT_TOKEN')
        self.bot = telebot.TeleBot(self.token)
        self.logger = telebot.logger
        telebot.logger.setLevel(log_level)
        if proxy:
            self.set_proxy(proxy)

        self.themes = {
            'Анекдоты': 1,
            'Рассказы': 2,
            'Стишки': 3,
            'Афоризмы': 4,
            'Цитаты': 5,
            'Тосты': 6,
            'Статусы': 8,
            'Анекдоты (+18)': 11,
            'Рассказы (+18)': 12,
            'Стишки (+18)': 13,
            'Афоризмы (+18)': 14,
            'Цитаты (+18)': 15,
            'Тосты (+18)': 16,
            'Статусы (+18)': 18,
        }
        self.last_message = None

    def set_proxy(self, proxy):
        self.logger.debug(f'Set bot proxy to: {proxy}')
        apihelper.proxy = proxy

    def setup_handlers(self):
        self.logger.info('Setup handlers for bot')
        # тут логика обработчиков

        def last_query_saver(func):
            """
            декоратор сохранения последнего запроса
            :param func:
            :return:
            """
            def wrapper(message):
                if self.last_message:
                    self.logger.debug(f'Run saved message: {self.last_message}')
                    func(self.last_message)
                else:
                    self.last_message = message

                func(message)

                self.last_message = None
            return wrapper

        @self.bot.message_handler(commands=['start', 'help'])
        def handle_start_help(message):
            self.logger.debug(message)

            buttons = self.themes.keys()
            markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
            for button in buttons:
                markup.row(button)
            self.bot.send_message(message.chat.id, JokeBot.about_text, reply_markup=markup)
            self.logger.info(f'Consuming message from user: {message.from_user.username}')

        @self.bot.message_handler(content_types=['text'])
        @last_query_saver
        def handle_joke_themes(message):
            if message.text in self.themes.keys():
                joke = self.get_fun_content(self.themes.get(message.text))
                self.bot.send_message(message.chat.id, joke)

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
        self.logger.info('Receive joke from external server')
        api_url = f'http://rzhunemogu.ru/RandJSON.aspx?CType={theme}'
        content = requests.get(api_url).content.decode('windows-1251')
        self.logger.debug(content)
        content = content[12:-2]
        # TODO: сделать 10 и 20 тему, это видео, нужно выдергивать ссылку на видео и отправлять в чат как видео
        return content


class BotLauncher:
    def __init__(self, bot_cls, log_level='INFO', use_proxies=False):
        self.logger = telebot.logger
        self.log_level = log_level
        telebot.logger.setLevel(self.log_level)
        self.bot_cls = bot_cls
        self.current_bot = bot_cls(log_level=self.log_level)
        if use_proxies:
            self.proxies = self.get_proxies()
        else:
            self.proxies = None

    def get_proxies(self):
        self.logger.info('Start finding proxies')
        proxies = from_cn_proxy() + from_cyber_syndrome() + from_free_proxy_list() + \
            from_hide_my_ip() + from_proxy_spy()

        self.logger.info('Testing proxies')
        result = freeproxy.test_proxies(proxies, 8, 'http://httpbin.org/get')
        result = [{'http': 'http://' + ip.strip(), 'https': 'https://' + ip.strip()} for ip in result]
        random.shuffle(result)
        return result

    def start(self):
        while True:
            self.logger.info('Starting bot')
            proxy = None
            if self.proxies:
                try:
                    proxy = self.proxies.pop()
                except IndexError:
                    self.logger.info('End of proxies list reached. Scan for new proxies')
                    self.proxies = self.get_proxies()
                    continue

            try:
                self.current_bot.set_proxy(proxy)
                self.current_bot.run()
            except (requests.exceptions.ProxyError, requests.exceptions.ConnectionError, ReadTimeoutError,
                    MaxRetryError) as e:
                self.logger.debug(e)
                self.logger.info('Restarting bot')
                continue


if __name__ == '__main__':
    launcher = BotLauncher(bot_cls=JokeBot, log_level='DEBUG')
    launcher.start()
