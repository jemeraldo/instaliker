# coding: utf8

# Headers
X_EVOTOR_USERID = 'X-Evotor-User-Id'
X_EVOTOR_DEVICEID = 'X-Evotor-Device-Uuid'
X_SCREENID = 'X-Screen-Id'
AUTH_TOKEN = 'Authorization'
X_AUTH_TOKEN = 'X-Authorization'

#DB
EVODB_NAME = 'evodb'

DB_APPS = 'apps'
DB_BINDS = 'binds'
DB_CASHIERS = 'cashiers'
DB_RATES = 'rates'
DB_SETTINGS = 'settings'
DB_RECS = 'recs'
DB_SLIDES = 'slides'

APPS_USERID = 'userId'
APPS_INSTALLED = 'installed'
APPS_TOKEN = 'token'

BINDS_DEVICEID = 'deviceid'
BINDS_CODE = 'code'
BINDS_SCREENID = 'screenid'
BINDS_IP = 'ip'
EVOTOR_BINDED = 'binded'
SCREEN_BINDED = 'binded'

CASHIERS_ID = 'cashierId'
CASHIERS_NAME = 'cashierName'

RATES_RATING = 'rating'
TIMESTAMP = 'timestamp'

SETTINGS_TELEGRAMUSERID = 'reportTelegramUserid'
SETTINGS_TCODE = 'telegramCode'
SETTINGS_TCHATID = 'tchat_id'

#ENDPOINTS

ep_binding = dict(url='/api/v1/binding', methods=['GET'])
ep_bind = dict(url='/api/v1/bind', methods=['POST'])
ep_evotor_binded = dict(url='/api/v1/evotor-binded', methods=['GET'])
ep_screen_binded = dict(url='/api/v1/screen-binded', methods=['GET'])
ep_unbind = dict(url='/api/v1/unbind', methods=['POST'])

ep_ip = dict(url='/api/v1/ip', methods=['GET', 'POST'])

ep_install_event = dict(url='/api/v1/install-event', methods=['POST'])
ep_token = dict(url='/api/v1/token', methods=['POST'])

ep_feedback = dict(url='/api/v1/feedback', methods=['POST'])
ep_screen_settings = dict(url='/api/v1/screen-settings', methods=['GET'])
ep_screen_recs = dict(url='/api/v1/screen-recs', methods=['GET'])
