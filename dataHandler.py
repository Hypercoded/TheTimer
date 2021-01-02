import pymongo

# Details
db_name = "timer_db"
db_password = "DB_PASSWORD"

# Connect to DB and retrieve the timer_data collection.
client = pymongo.MongoClient(
    f"mongodb+srv://TheTimer:{db_password}@cluster0.4hk3a.mongodb.net/{db_name}?retryWrites=true&w=majority")

db = client.get_database("timer_db")
data = db.timer_data

# Format for documents
statsDoc = {
    "type": "stats",

    "cumulativeSeconds": 0,
    "seconds_from_subscribers": 0,
    "seconds_from_comments": 0,
    "seconds_from_likes": 0,
    "seconds_from_views": 0,

    "totalInteractions": 0,
    "total_subscribers": 0,
    "total_comments": 0,
    "total_likes": 0,
    "total_views": 0,

    "seconds_left": 0,
    "endDate": "",
    "endDateFormatted": ""

}

settingsDoc = {
    "type": "settings",

    "subscribersWeight": 28800,
    "commentsWeight": 10800,
    "likesWeight": 3600,
    "viewsWeight": 1800,

    "startingDate": "1-1-2021 00:00:00",
    "startingTime": 86400,
    "videoID": ""


}

thresholdDoc = {
    "type": "threshold",

    "timestamp": "",

    "subscribers": 0,
    "comments": 0,
    "likes": 0,
    "views": 0,

}


# If documents are not already created, make them. If not, then load the docs to a local copy
def refreshData():
    global statsDoc
    global settingsDoc
    global thresholdDoc

    if data.find_one({"type": "stats"}) is None:
        data.insert_one(statsDoc)
    else:
        statsDoc = data.find_one({"type": "stats"})

    if data.find_one({"type": "settings"}) is None:
        data.insert_one(settingsDoc)
    else:
        settingsDoc = data.find_one({"type": "settings"})

    if data.find_one({"type": "threshold"}) is None:
        data.insert_one(thresholdDoc)
    else:
        thresholdDoc = data.find_one({"type": "threshold"})


def calculate_total():
    refreshData()

    cumulativeSeconds = statsDoc["seconds_from_subscribers"] + statsDoc["seconds_from_comments"] + \
                        statsDoc["seconds_from_likes"] + statsDoc["seconds_from_views"]

    totalInteractions = statsDoc["total_subscribers"] + statsDoc["total_comments"] + statsDoc["total_likes"] + statsDoc[
        "total_views"]

    modify_stats("cumulativeSeconds", cumulativeSeconds)
    modify_stats("totalInteractions", totalInteractions)


def retrieve_stats(key):
    refreshData()
    return statsDoc[key]


def retrieve_settings(key):
    refreshData()
    return settingsDoc[key]


def retrieve_threshold(key):
    refreshData()
    return thresholdDoc[key]


def modify_setting(key, value):
    settingsDoc[key] = value
    data.update_one({"type": "settings"}, {"$set": {key: value}})


def modify_stats(key, value):
    statsDoc[key] = value
    data.update_one({"type": "stats"}, {"$set": {key: value}})


def modify_threshold(key, value):
    thresholdDoc[key] = value
    data.update_one({"type": "threshold"}, {"$set": {key: value}})


refreshData()
