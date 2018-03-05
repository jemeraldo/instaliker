import os
from configparser import RawConfigParser, NoOptionError
from instabot import Bot
import logging
import time
import random
import schedule
import threading
import like_medias_by_location2 as lmbloc

project_delay = 5

def run_threaded(job_fn):
    job_thread = threading.Thread(target=job_fn)
    job_thread.start()
            
class Project(object):
    def __init__(self, name):
        self.name = name
        
    def __str__(self):
        return 'Project ' + self.name
        
    def get_random(from_list):
        _random = random.choice(from_list)
        return _random    
    
    def like_hashtag_fn(self):
        amount = self.like_hashtag_amount
        self.bot.logger.info("like_hashtag started, amount = %s" % str(amount))
        if self.like_random_tag:
            ht = get_random(self.hashtags)
        else:
            ht = self.hashtags[self.like_hashtag_counter % len(self.hashtags)]
            self.like_hashtag_counter += 1
        
        self.bot.like_hashtag(ht, amount=amount)
        self.bot.logger.info("like_hashtag job done")
    
    def like_hashtag_feed_job(self):
        schedule.every(self.like_hashtag_period).minutes.do(run_threaded, self.like_hashtag_fn)
        run_threaded(self.like_hashtag_fn)

    def like_geotag_fn(self):
        amount = self.like_geotag_amount
        self.bot.logger.info("like_first_lication_feed started, amount = %s" % str(amount))
        if self.like_random_tag:
            loc = get_random(self.geotags)
        else:
            loc = self.geotags[self.like_geotag_counter % len(self.geotags)]
            self.like_geotag_counter += 1
        
        lmbloc.like_first_location_feed(self.bot, loc, amount=amount)
        self.bot.logger.info("like_first_lication_feed job done")
        
    def like_geotag_feed_job(self):
        schedule.every(self.like_geotag_period).minutes.do(run_threaded, self.like_geotag_fn)
        run_threaded(self.like_geotag_fn)
        
    def save_stats_fn(self):
        self.bot.save_user_stats(self.bot.user_id)
        
    def save_stats_job(self):
        schedule.every(self.save_stats_period).minutes.do(run_threaded, self.save_stats_fn)
        
        
    def loadCfg(self):
        cfg = RawConfigParser()
        cfg.read('./projects/' + self.name + '/config.ini', encoding='utf-8')
        self.StopWords = eval(cfg.get('Project', 'StopWords', fallback='tuple()'))
        self.jobs = []
        
        if cfg.getboolean('Tasks', 'LikeHashtagFeed', fallback=False):
            self.jobs += [self.like_hashtag_feed_job]
        if cfg.getboolean('Tasks', 'LikeGeotagFeed', fallback=False):
            self.jobs += [self.like_geotag_feed_job]
        if cfg.getboolean('Tasks', 'SaveStats', fallback=False):
            self.jobs += [self.save_stats_job]
        self.like_hashtag_amount = int(eval(cfg.get('Tasks', 'LikeHashtagAmount', fallback='700 / 24')))
        self.like_hashtag_period = int(eval(cfg.get('Tasks', 'LikeHashtagPeriod', fallback='60')))
        self.like_geotag_amount = int(eval(cfg.get('Tasks', 'LikeGeotagAmount', fallback='700 / 24')))
        self.like_geotag_period = int(eval(cfg.get('Tasks', 'LikeGeotagPeriod', fallback='60')))
        self.save_stats_period = int(eval(cfg.get('Tasks', 'SaveStatsPeriod', fallback='120')))
        
        self.uname = cfg.get('Main', 'uname')
        self.upass = cfg.get('Main', 'upass')
        
        self.like_random_tag = False
        
    def startBot(self):
        self.bot = Bot(comments_file='./projects/' + self.name + '/comments.txt',
            blacklist='./projects/' + self.name + '/blacklist.txt',
            whitelist='./projects/' + self.name + '/whitelist.txt',
            stop_words=self.StopWords)
        
        #Logger
        self.bot.logger = logging.getLogger('[instabot-' + self.name + ']')
        self.bot.logger.setLevel(logging.DEBUG)
        
        if len(self.bot.logger.handlers) > 0:
            ch = self.bot.logger.handlers[0]
        else:
            ch = logging.StreamHandler()
            self.bot.logger.addHandler(ch)
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[' + self.name + ' %(threadName)s] %(asctime)s - %(levelname)s: %(message)s')
        ch.setFormatter(formatter)

        self.bot.login(username=self.uname, password=self.upass)
        self.bot.logger.info("Project " + self.name + ' bot started, jobs: ' + str(self.jobs))

        #self.random_users = bot.read_list_from_file(config.USERS_FILE)
        self.hashtags = self.bot.read_list_from_file('./projects/' + self.name + '/hashtag_database.txt')
        self.geotags = self.bot.read_list_from_file('./projects/' + self.name + '/geotag_database.txt')
        #random_locations_file = bot.read_list_from_file(config.LOCATIONS_FILE)
        #photo_captions = bot.read_list_from_file(config.PHOTO_CAPTIONS_FILE)
        
        #Counters
        self.like_hashtag_counter = 0
        self.like_geotag_counter = 0

        for job_fn in self.jobs:
            job_fn()

        
if __name__=='__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(threadName)s: %(message)s',
                    filename='instabot.log',
                    level=logging.INFO
                    )

    projects = []
    for proj in os.listdir('./projects/'):
        pobj = Project(proj)
        pobj.loadCfg()
        projects += [pobj]
        
    for proj in projects:
        proj.startBot()
        time.sleep(project_delay)