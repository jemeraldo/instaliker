# -*- coding: utf-8 -*-
import schedule
import time
import sys
import os
import random
import glob             # ->added to make pics upload -> see job8
import threading        # ->added to make multithreadening possible -> see fn run_threaded
import logging

#sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot

import config
import like_medias_by_location2 as lmbloc


bot = Bot(comments_file=config.COMMENTS_FILE, blacklist=config.BLACKLIST_FILE, whitelist=config.WHITELIST_FILE,
          stop_words=('shop', 'store', 'магазин', 'купить', 'заработок', 'аренда', 'заказать', 'доставка',
                      'бронирование'))

bot.logger = logging.getLogger('[instabot]')
bot.logger.setLevel(logging.DEBUG)
logging.basicConfig(format='%(asctime)s - %(threadName)s: %(levelname)s - %(message)s',
                    filename='instabot.log',
                    level=logging.INFO
                    )
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(threadName)s: %(levelname)s - %(message)s')
ch.setFormatter(formatter)
bot.logger.addHandler(ch)

bot.login(username=config.UNAME, password=config.UPASS)
bot.logger.info("like by schedule script. 1 hour save")

random_user_file = bot.read_list_from_file(config.USERS_FILE)
random_hashtag_file = bot.read_list_from_file(config.HASHTAGS_FILE)
random_locations_file = bot.read_list_from_file(config.LOCATIONS_FILE)
photo_captions = bot.read_list_from_file(config.PHOTO_CAPTIONS_FILE)


# Return a random value from a list, used in various jobs below
def get_random(from_list):
    _random = random.choice(from_list)
    return _random


def stats():
    bot.save_user_stats(bot.user_id)


def tema_hashtag():
    amount = int(700 / 24 / 2)
    bot.logger.info("like_hashtag started, amount = %s" % str(amount))
    bot.like_hashtag(get_random(random_hashtag_file), amount=amount)
    bot.logger.info("like_hashtag job done")


def tema_geotag():
    amount = int(700 / 24 / 2)
    bot.logger.info("like_first_lication_feed started, amount = %s" % str(amount))
    lmbloc.like_first_location_feed(bot, get_random(random_locations_file), amount=amount)
    bot.logger.info("like_first_lication_feed job done")


# function to make threads -> details here http://bit.ly/faq_schedule
def run_threaded(job_fn):
    job_thread = threading.Thread(target=job_fn)
    job_thread.start()


schedule.every(1).hour.do(run_threaded, stats)              # get stats
schedule.every(1).hours.do(run_threaded, tema_hashtag)              # like hashtag
schedule.every(1).hours.do(run_threaded, tema_geotag)              # like locations

run_threaded(tema_hashtag)
run_threaded(tema_geotag)

#tema_hashtag()
#tema_geotag()

while True:
    schedule.run_pending()
    time.sleep(1)
