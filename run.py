# coding: utf8
import json, random, os, sys
import settings
from eve import Eve
from flask import request, render_template
from pymongo import MongoClient, errors as mongo_errors
from evotor_settings import *
from evodb import *
import tbot
from bson.json_util import dumps
from bson.objectid import ObjectId

debug_mode = True
do_test = False

app = Eve()
client = MongoClient(settings.MONGO_URI)
db = client[EVODB_NAME]
server_port = os.environ.get('PORT', 5000)

def print_debug_info():
    if debug_mode:
        print(request.headers)
        print(request.data)

def json_response(body, status=200, **headers):
    s = json.dumps(body)
    resp = app.make_response((s, status, headers))

    resp.headers.set("Content-Type", "Application/json")
    return resp

def json_error(text, status=400, **headers):
    return json_response({'error': text}, status, **headers)

def check_headers(*headers):
    for h in headers:
        res = request.headers.get(h)
        if res is None:
            return h
    return None

def check_data(*datafields):
    if not request.data and datafields:
        return datafields[0]
    D = json.loads(request.data)
    for df in datafields:
        res = D[df]
        if res is None:
            return df
    return None

'''
@app.route(ep_install_event['url'], methods=ep_install_event['methods'])
def install_event():
    print_debug_info()
    data = json.loads(request.data)
    userid = data['data'][APPS_USERID]
    installed = 1 if data['type'] == 'ApplicationInstalled' else 0
    timestamp = data[TIMESTAMP]
    if app_install(None, userid, timestamp, installed):
        return json_response({'status': 'ok'}, 200)

    return json_error('error')
'''

@app.route(ep_token['url'], methods=ep_token['methods'])
def token_event():
    print_debug_info()
    try:
        data = json.loads(request.data)
        token = data[APPS_TOKEN]
        userid = data[APPS_USERID]
        set_token(userid, token)
        return json_response({'status': 'ok'}, 200)
    except Exception:
        print(token, userid)
        return json_response('error while getting token')

@app.route(ep_binding['url'], methods=ep_binding['methods'])
def initiate_binding():
    print_debug_info()

    ch = check_headers(X_EVOTOR_DEVICEID, X_EVOTOR_USERID)
    if ch is not None:
        return json_error('No header ' + ch + ' provided')

    userid = request.headers.get(X_EVOTOR_USERID)
    deviceid = request.headers.get(X_EVOTOR_DEVICEID)

    try:
        result = add_new_bind(deviceid, userid)
        return json_response({BINDS_CODE: result[BINDS_CODE]}, 200)
    except Exception as e:
        return json_error('Error while adding new bind')


@app.route(ep_bind['url'], methods=ep_bind['methods'])
def bind_screen():
    print_debug_info()
    ch = check_headers(X_SCREENID)
    if ch is not None:
        return json_error('No header ' + ch + ' provided')
    ch = check_data(BINDS_CODE)
    if ch is not None:
        return json_error('No field "' + ch + '" provided')

    code = json.loads(request.data)[BINDS_CODE]
    screenid = request.headers.get(X_SCREENID)

    binds = db[DB_BINDS]
    item = binds.find_one({BINDS_CODE: code})
    if item is None:
        return json_error('Wrong code')

    try:
        item = set_bind(code, screenid)
    except Exception as e:
        return json_error('error while setting bind: ' + str(e))

    return json_response(
        {
            EVOTOR_BINDED: True, BINDS_IP: item[BINDS_IP], BINDS_DEVICEID: item[BINDS_DEVICEID]
        }, 200)

@app.route(ep_evotor_binded['url'], methods=ep_evotor_binded['methods'])
def evotor_binded():
    print_debug_info()
    ch = check_headers(X_EVOTOR_DEVICEID)
    if ch:
        return json_error('No header ' + X_EVOTOR_DEVICEID + ' provided')

    deviceid = request.headers.get(X_EVOTOR_DEVICEID)
    return json_response({EVOTOR_BINDED: is_device_binded(deviceid)})


@app.route(ep_screen_binded['url'], methods=ep_screen_binded['methods'])
def screen_binded():
    print_debug_info()
    ch = check_headers(X_SCREENID)
    if ch:
        return json_error('No header ' + X_SCREENID + ' provided')

    screenid = request.headers.get(X_SCREENID)
    return json_response({SCREEN_BINDED: is_screen_binded(screenid)})

@app.route(ep_unbind['url'], methods=ep_unbind['methods'])
def unbind():
    print_debug_info()
    ch = check_headers(X_EVOTOR_DEVICEID)
    if ch:
        return json_error('No header ' + X_EVOTOR_DEVICEID + ' provided')
    deviceid = request.headers.get(X_EVOTOR_DEVICEID)

    item = db[DB_BINDS].find_one({BINDS_DEVICEID: deviceid})
    if not item:
        return json_error('No such bind in database')
    try:
        unbind_screen(deviceid)
        return json_response({SCREEN_BINDED: False})
    except Exception as e:
        return json_error('Error while unbinding')

@app.route(ep_ip['url'], methods=ep_ip['methods'])
def setgetip():
    print_debug_info()
    if request.method == 'POST':
        ch = check_headers(X_SCREENID)
        if ch:
            return json_error('No header ' + X_SCREENID + ' provided')
        screenid = request.headers.get(X_SCREENID)
        ch = check_data(BINDS_IP)
        if ch:
            return json_error('No field "' + ch + '" provided')
        ip = json.loads(request.data)[BINDS_IP]

        item = db[DB_BINDS].find_one({BINDS_SCREENID: screenid})
        if not item:
            return json_error('No such screen in database')
        try:
            if set_ip(screenid, ip):
                return json_response({'status': 'ok'})
        except Exception as e:
            return json_error('error while setting ip')
    if request.method == 'GET':
        ch = check_headers(X_EVOTOR_DEVICEID)
        if ch:
            return json_error('No header ' + X_EVOTOR_DEVICEID + ' provided')
        deviceid = request.headers.get(X_EVOTOR_DEVICEID)
        item = db[DB_BINDS].find_one({BINDS_DEVICEID: deviceid})
        if not item:
            return json_error('No such screen in binds')

        ip = get_ip(deviceid)

        if ip:
            return json_response({BINDS_IP: ip}, 200)
        else:
            return json_error('Screen has not binded to any evotor device')

@app.route(ep_feedback['url'], methods=ep_feedback['methods'])
def post_feedback():
    print_debug_info()
    ch = check_headers(X_SCREENID)
    if ch:
        return json_error('No header ' + X_SCREENID + ' provided')
    screenid = request.headers.get(X_SCREENID)

    ch = check_data(CASHIERS_ID, RATES_RATING, TIMESTAMP)
    if ch:
        return json_error('No field "' + ch + '" provided')

    data = json.loads(request.data)
    cid = data[CASHIERS_ID]
    rating = data[RATES_RATING]
    timestamp = data[TIMESTAMP]
    print(cid, rating, timestamp)
    item = db[DB_CASHIERS].find_one({CASHIERS_ID: cid})
    if item:
        cashierName = item[CASHIERS_NAME]
        userid = item[APPS_USERID]
    else:
        item = db[DB_BINDS].find_one({BINDS_SCREENID: screenid})
        userid = item[APPS_USERID]
        get_cashiers_list(userid)
        item = db[DB_CASHIERS].find_one({CASHIERS_ID: cid})
        if not item:
            return json_error('No such cashier')
        cashierName = db[DB_CASHIERS].find_one({CASHIERS_ID: cid})[CASHIERS_NAME]


    try:
        add_feedback(cid, rating, timestamp)
        chat_id = get_settings_telegram_chat_id(userid)
        tbot.send_feedback(chat_id, cashierName, rating)
    except Exception:
        print(Exception)
        return json_error('Error while post feedback')

    return json_response({'status': 'ok'})

@app.route(ep_screen_settings['url'], methods=ep_screen_settings['methods'])
def screen_settings():
    print_debug_info()
    ch = check_headers(X_SCREENID)
    if ch:
        return json_error('No header ' + X_SCREENID + ' provided')
    screenid = request.headers.get(X_SCREENID)
    item = db[DB_BINDS].find_one({BINDS_SCREENID: screenid})
    if not item:
        return json_error('No such screen in db')

    userid = item[APPS_USERID]
    item = db[DB_SETTINGS].find_one({APPS_USERID: userid})
    if not item:
        json_error('No settings for screen ' + screenid)

    return dumps(item)


@app.route('/user-settings', methods=['GET', 'POST'])
def user_settings():
    if request.method == 'GET':
        userid = request.args.get(APPS_USERID)
        if not userid:
            return 'Wait for url parameter: userId'
        item = db[DB_SETTINGS].find_one({APPS_USERID: userid})
        recs = db[DB_RECS].find({APPS_USERID: userid})
        cashiersStats = get_cashiers_stats(userid)
        if not item:
            return 'Can\'t find settings for ' + userid
        return render_template('settings.html', item=item, recs=recs, cashiersStats=cashiersStats)
    if request.method == 'POST':
        userid = request.args.get(APPS_USERID)
        adType = request.form['adType']
        feedbackType = request.form['feedbackType']
        text = request.form['text']
        adVideoUrl = request.form['adVideoUrl']

        res = db[DB_SETTINGS].update_one({APPS_USERID: userid}, {'$set': {'adType': adType, 'feedbackType': feedbackType,\
                                                                          'text': text, 'adVideoUrl': adVideoUrl}})
        item = db[DB_SETTINGS].find_one({APPS_USERID: userid})
        recs = db[DB_RECS].find({APPS_USERID: userid})
        cashiersStats = get_cashiers_stats(userid)

        return render_template('settings.html', item=item, recs=recs, saved=True, cashiersStats=cashiersStats)

@app.route('/add-rec', methods=['POST'])
def add_rec():
    userid = request.args.get(APPS_USERID)
    if not userid:
        return 'No userid provided'

    timestart = request.form['timestart']
    timeend = request.form['timeend']
    keywords = request.form['keywords'].rstrip(',').split(',')
    kwmethod = request.form['kwmethod']
    text = request.form['text']
    productId = request.form['productId']
    discount = request.form['discount']

    res = db[DB_RECS].insert_one({APPS_USERID: userid, 'timestart': timestart,\
            'timeend': timeend, 'keywords': keywords, 'kwmethod': kwmethod,\
            'text': text, 'productId': productId, 'discount': discount})

    item = db[DB_SETTINGS].find_one({APPS_USERID: userid})
    recs = db[DB_RECS].find({APPS_USERID: userid})
    cashiersStats = get_cashiers_stats(userid)
    return render_template('settings.html', item=item, recs=recs, recadded=True, cashiersStats=cashiersStats)

@app.route('/del-rec', methods=['POST'])
def del_rec():
    userid = request.args.get('userId')
    recid = request.args.get('recid')

    #rec = db[DB_RECS].find_one({'_id': recid})
    item = db[DB_RECS].find_one({'_id': ObjectId(recid)})
    print(item)
    res = db[DB_RECS].delete_one({'_id': ObjectId(recid)})


    item = db[DB_SETTINGS].find_one({APPS_USERID: userid})
    recs = db[DB_RECS].find({APPS_USERID: userid})
    cashiersStats = get_cashiers_stats(userid)


    return render_template('settings.html', item=item, recs=recs, cashiersStats=cashiersStats, recdeleted=True)

@app.route(ep_screen_recs['url'], methods=ep_screen_recs['methods'])
def screen_recs():
    print_debug_info()
    ch = check_headers(X_SCREENID)
    if ch:
        return json_error('No header ' + X_SCREENID + ' provided')

    screenid = request.headers.get(X_SCREENID)
    item = db[DB_BINDS].find_one({BINDS_SCREENID: screenid})
    if not item:
        return json_error('No such screen in db')

    userid = item[APPS_USERID]
    items = db[DB_RECS].find({APPS_USERID: userid})

    return dumps(items)

def run_tests():
    add_new_bind('ev-99122331', '99-945749584759345')
    add_new_bind('ev-00011233', '99-945749584759315')
    add_new_bind('ev-00112234', '99-945749184759315')
    bc2 = db[DB_BINDS].find_one({BINDS_DEVICEID: 'ev-00011233'})[BINDS_CODE]
    bc3 = db[DB_BINDS].find_one({BINDS_DEVICEID: 'ev-00112234'})[BINDS_CODE]
    set_bind(bc2, 'sc-111')
    set_bind(bc3, 'sc-123')
    unbind_screen(bc2)
    set_ip('ev-00112234', '192.168.14.19')
    set_token('01-115411292457301', 'f46b89a5-8e80-4591-b0aa-94551790444b')
    print('Device ev-99122331 is binded: ', is_device_binded('ev-99122331'))
    print('Device ev-00011233 is binded: ', is_device_binded('ev-00011233'))
    print('Device ev-00112234 is binded: ', is_device_binded('ev-00112234'))
    print('Screen sc-111 is binded: ', is_screen_binded('sc-111'))
    print('Screen sc-123 is binded: ', is_screen_binded('sc-123'))
    print('Screen sc-123 gets evotor ip: ', get_ip('sc-123'))

def init_db():
    binds = db[DB_BINDS]
    indexes = binds.index_information()
    if BINDS_DEVICEID not in indexes:
        binds.create_index(BINDS_DEVICEID, unique=True)

if __name__ == '__main__':
    init_db()
    if do_test:
        run_tests()
    app.run(host='0.0.0.0', port=server_port)
    tbot.updater.stop()

