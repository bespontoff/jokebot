# -*- coding: UTF-8 -*-
__author__ = 'bespontoff'

import telebot

token = '237625759:AAFAgX-oY_lelc1X27PYRZFw0dCykfdR_Qk'


class JokeBot:
    def __init__(self):
        self.bot = telebot.TeleBot(token)


if __name__ == '__main__':
    jb = JokeBot()
    jb.bot.get_me()