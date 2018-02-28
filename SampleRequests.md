### http GET :5000/api/v1/settings/
HTTP/1.0 200 OK

### http POST :5000/api/v1/settings userId=01-115411292457301 adType=text text="Рекламный текст" reportTelegramUserid=\@Avtyu
HTTP/1.0 201 CREATED
Response:
{
    "_created": "Fri, 01 Dec 2017 11:41:44 GMT",
    "_id": "5a213ff86c269d036ce8b5f4",
    "_links": {
        "self": {
            "href": "settings/5a213ff86c269d036ce8b5f4",
            "title": "user-settings"
        }
    },
    "_status": "OK",
    "_updated": "Fri, 01 Dec 2017 11:41:44 GMT"
}

### http GET :5000/api/v1/settings/01-115411292457301
Response:
{
    "_created": "Fri, 01 Dec 2017 11:41:44 GMT",
    "_id": "5a213ff86c269d036ce8b5f4",
    "_links": {
        "collection": {
            "href": "settings",
            "title": "settings"
        },
        "parent": {
            "href": "/",
            "title": "home"
        },
        "self": {
            "href": "settings/5a213ff86c269d036ce8b5f4",
            "title": "user-settings"
        }
    },
    "_updated": "Fri, 01 Dec 2017 11:41:44 GMT",
    "adType": "text",
    "adVideoUrl": "https://www.youtube.com/watch?v=sQZKiDIzft8&t=0s",
    "feedbackType": "none",
    "reportTelegramUserid": "@Avtyu",
    "ssDelay": 10,
    "text": "Рекламный текст",
    "userId": "01-115411292457301"
}

### http DELETE :5000/api/v1/settings/5a2140936c269d036ce8b5f5
Response:
HTTP/1.0 204 NO CONTENT

### http PATCH :5000/api/v1/settings/5a214ad56c269d0dece4631c text="New ad-text"
Response:
HTTP/1.0 200 OK
{
    "_created": "Fri, 01 Dec 2017 12:28:04 GMT",
    "_id": "5a214ad56c269d0dece4631c",
    "_links": {
        "self": {
            "href": "settings/5a214ad56c269d0dece4631c",
            "title": "user-settings"
        }
    },
    "_status": "OK",
    "_updated": "Fri, 01 Dec 2017 12:29:09 GMT"
}

### http POST :5000/api/v1/recs userId=01-115411292457301 keywords:="[\"pasta\", \"sauce\"]" kwmethod=all text=mozarella
Response:
HTTP/1.0 201 CREATED
{
    "_created": "Fri, 01 Dec 2017 12:05:49 GMT",
    "_id": "5a21459d6c269d06fc3279bb",
    "_links": {
        "self": {
            "href": "recs/5a21459d6c269d06fc3279bb",
            "title": "rec"
        }
    },
    "_status": "OK",
    "_updated": "Fri, 01 Dec 2017 12:05:49 GMT"
}

### http PATCH :5000/api/v1/recs/5a2145296c269d06fc3279ba text=somerec
Response:
HTTP/1.0 200 OK
{
    "_created": "Fri, 01 Dec 2017 12:03:53 GMT",
    "_id": "5a2145296c269d06fc3279ba",
    "_links": {
        "self": {
            "href": "recs/5a2145296c269d06fc3279ba",
            "title": "rec"
        }
    },
    "_status": "OK",
    "_updated": "Fri, 01 Dec 2017 12:08:39 GMT"
}

### 

### http DELETE :5000/api/v1/slides/5a21693c6c269d13bc77f5ca
Response:
HTTP/1.0 204 NO CONTENT