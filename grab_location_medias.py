import schedule
import time
import sys
import os
import random
import glob             # ->added to make pics upload -> see job8
import threading        # ->added to make multithreadening possible -> see fn run_threaded
import logging
from instabot import Bot
import config

def distance_in_km(long1, lat1, long2, lat2):
    import math  # Можно поместить в блок импортов основного файла
    d2r = math.pi / 180.0
    # phi = 90 - широта
    phi1 = (90.0 - lat1) * d2r
    phi2 = (90.0 - lat2) * d2r
         
    # theta = долгота
    theta1 = long1 * d2r
    theta2 = long2 * d2r
    carc = (math.sin(phi1) * math.sin(phi2) * math.cos(theta1 - theta2) +
           math.cos(phi1) * math.cos(phi2))
    return math.acos(carc) * 6371


def get_loc_by_coords(self, lat, lng, city='', distance_limit=50):
    self.searchLocation(lat=lat, lng=lng)
    distance = lambda location: distance_in_km(lng, lat, location["location"]["lng"], location["location"]["lat"])
    #return [location for location in self.LastJson["items"] if int(location["location"]["lat"]) == #int(latitude) and
    #        int(location["location"]["lng"]) == int(longitude)]
    if city:
        return [location for location in self.LastJson['items'] if location['location']['city'] == city]
    else:
        return [location for location in self.LastJson['items'] if int(distance(location))<=int(distance_limit)]

def get_list_locs_by_coords(self, lat, lng, city='', distance_limit=50):
    locs = get_loc_by_coords(self, lat, lng, city=city, distance_limit=distance_limit)
    for loc in locs:
        print(loc['location']['short_name'])
        
def get_location_medias_from_coordinates(self, lat, lng, distance_limit=50):
    #проходим по всем локациям, собираем ВСЕ media
    #2 вариант: проходим по локациям, собираем только новые media. Стоп-флаг, если любое media уже есть в списке
    pass
        
bot = Bot(comments_file=config.COMMENTS_FILE, blacklist=config.BLACKLIST_FILE, whitelist=config.WHITELIST_FILE, stop_words=config.STOP_WORDS)
               
bot.logger = logging.getLogger('[instabot]')
bot.logger.setLevel(logging.DEBUG)
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(threadName)s: %(message)s',
                    filename='instabot.log',
                    level=logging.INFO
                    )
ch = bot.logger.handlers[0]
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(threadName)s: %(message)s')
ch.setFormatter(formatter)

bot.login(username=config.UNAME, password=config.UPASS)
bot.logger.info("grab location medias script starts")

