# coding=utf-8
"""
    instabot example

    Workflow:
        Like medias by location.
"""

import argparse
import codecs
import os
import sys

from tqdm import tqdm


sys.path.append(os.path.join(sys.path[0], '../../'))
from instabot import Bot


def like_location_feed(new_bot, new_location, amount=0, quiet=True):
    counter = 0
    max_id = ''
    with tqdm(total=amount) as pbar:
        while counter < amount:
            if new_bot.getLocationFeed(new_location['location']['pk'], maxid=max_id):
                location_feed = new_bot.LastJson
                for media in new_bot.filter_medias(location_feed["items"][:amount], quiet=True):
                    if not quiet:
                        new_bot.logger.info("Liking media %s" % media)
                    if new_bot.like(media):
                        if not quiet:
                            new_bot.logger.info("Media %s was liked" % media)
                        counter += 1
                        pbar.update(1)
                if location_feed.get('next_max_id'):
                    max_id = location_feed['next_max_id']
                else:
                    return False
    return True


def like_first_location_feed(bot, location, amount, quiet=True):
    bot.logger.info("Looking for location %s" % location)
    bot.searchLocation(location)
    finded_location = bot.LastJson['items'][0]
    if finded_location:
        bot.logger.info(u"Found {}".format(finded_location['title']))

        like_location_feed(bot, finded_location, amount=amount, quiet=quiet)
    else:
        bot.logger.info("%s not found" % location)

if __name__ == "__main__":
    #stdout = sys.stdout
    #sys.stdout = codecs.getwriter('utf8')(sys.stdout)

    #try:
    #    input = raw_input
    #except NameError:
    #    pass

    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('-u', type=str, help="username")
    parser.add_argument('-p', type=str, help="password")
    parser.add_argument('-amount', type=str, help="amount")
    parser.add_argument('-proxy', type=str, help="proxy")
    parser.add_argument('locations', type=str, nargs='*', help='locations')
    args = parser.parse_args()

    try:
        print(u'Like medias by location')
    except TypeError:
        sys.stdout = stdout

    bot = Bot(stop_words=('shop', 'store', 'free', 'магазин', 'купить', 'заработок', 'аренда', 'заказать', 'доставка',
                      'бронирование', 'вилла'))
    bot.login(username=args.u, password=args.p,
              proxy=args.proxy)

    if args.locations:
        for location in args.locations:
            like_first_location_feed(bot, location, int(args.amount))

    else:
        print("No locations")

