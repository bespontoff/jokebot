# -*- coding: UTF-8 -*-
__author__ = 'bespontoff'

import logging

import telebot
from telebot import apihelper

token = '237625759:AAFAgX-oY_lelc1X27PYRZFw0dCykfdR_Qk'
proxies = {
    'http': 'http://51.15.6.77:5836',
    'https': 'https://51.15.6.77:5836',
}


class JokeBot:
    def __init__(self, proxy=None, log_level='INFO'):
        self.bot = telebot.TeleBot(token)
        self.logger = telebot.logger
        telebot.logger.setLevel(log_level)
        if proxy:
            apihelper.proxy = proxy


if __name__ == '__main__':
    jb = JokeBot(proxy=proxies, log_level='DEBUG')
    jb.bot.get_me()
