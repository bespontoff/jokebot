# -*- coding: UTF-8 -*-
__author__ = 'bespontoff'

import os
from unittest import TestCase, skip
from main import JokeBot, BotLauncher
from telebot import apihelper
from unittest.mock import Mock, patch


class JokebotTests(TestCase):
    def setUp(self) -> None:
        os.environ['TG_BOT_TOKEN'] = 'token898427985789'
        self.proxy = {'http': 'http://0.0.0.0', 'https': 'https://0.0.0.0'}

    def test_get_token_from_environ(self):
        bot = JokeBot()
        token = os.environ.get('TG_BOT_TOKEN')
        self.assertEqual(bot.token, token)

    def test_bot_can_use_proxy(self):
        JokeBot(proxy=self.proxy)
        self.assertEqual(apihelper.proxy, self.proxy)

    @patch('requests.get')
    def test_get_fun_content_return_joke(self, get_mock):
        response = Mock()
        response.content = '123412341234joke12'.encode('windows-1251')
        get_mock.return_value = response
        bot = JokeBot()
        joke = bot.get_fun_content(1)
        self.assertTrue(get_mock.called)
        self.assertEqual(joke, 'joke')


class BotLauncherTests(TestCase):
    def setUp(self) -> None:
        pass

    @patch('main.BotLauncher.get_proxies')
    def test_launcher_use_get_proxies(self, get_proxies_mock):
        bot = BotLauncher(JokeBot, use_proxies=True)
        self.assertTrue(get_proxies_mock.called)