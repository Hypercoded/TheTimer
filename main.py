import dataHandler
import apiHandler
import datetime
import time
from dateutil.relativedelta import relativedelta

CHANNEL_ID = "UCjYr2rHyKLzjL5iJQTfrPhw"
VIDEO_ID = dataHandler.retrieve_settings("videoID")


def recalculate(channelid, videoid):
    startDate = dataHandler.retrieve_settings("startingDate")
    starter_date = datetime.datetime.strptime(startDate, '%m-%d-%Y %H:%M:%S')

    current_date = datetime.datetime.now()

    currentTime = current_date.strftime('%m-%d-%Y %H:%M:%S')

    difference = current_date - starter_date

    if difference.total_seconds() > 0:
        try:
            yt_stats = apiHandler.get_stats(channelid, videoid)

            if difference.total_seconds() >= 0:
                # if its actually past the starting time, modify the stats, calculate cumulative time, and then change the threshold

                dataHandler.refreshData()

                thresholds = dataHandler.thresholdDoc
                settings = dataHandler.settingsDoc
                stats = dataHandler.statsDoc

                for category in ["subscribers", "comments", "likes", "views"]:
                    if int(yt_stats[category]) > thresholds[category]:
                        stats_difference = int(yt_stats[category]) - thresholds[category]

                        secondsToAdd = stats_difference * settings[f"{category}Weight"]

                        dataHandler.modify_stats(f"seconds_from_{category}",
                                                 secondsToAdd + stats[f"seconds_from_{category}"])
                        dataHandler.modify_stats(f"total_{category}", stats_difference + stats[f"total_{category}"])

            dataHandler.calculate_total()
            dataHandler.modify_threshold("timestamp", currentTime)
            dataHandler.modify_threshold("subscribers", int(yt_stats["subscribers"]))
            dataHandler.modify_threshold("comments", int(yt_stats["comments"]))
            dataHandler.modify_threshold("likes", int(yt_stats["likes"]))
            dataHandler.modify_threshold("views", int(yt_stats["views"]))

            totalSeconds = dataHandler.retrieve_stats("cumulativeSeconds")

            x = datetime.datetime.now()
            y = x + datetime.timedelta(0, totalSeconds + dataHandler.retrieve_settings(
                "startingTime") - difference.total_seconds())

            dataHandler.modify_stats("seconds_left", totalSeconds + dataHandler.retrieve_settings(
                "startingTime") - difference.total_seconds())
            dataHandler.modify_stats("endDate", y.strftime('%m-%d-%Y %H:%M:%S'))
            dataHandler.modify_stats("endDateFormatted", formatDate(y.strftime('%m-%d-%Y %H:%M:%S')))

            print(totalSeconds + dataHandler.retrieve_settings("startingTime") - difference.total_seconds())
            if (totalSeconds + dataHandler.retrieve_settings(
                    "startingTime") - difference.total_seconds()) < 0:
                apiHandler.delete_video(VIDEO_ID)
                print("video_deleted")
            return ()
        finally:
            print("Error")


def formatDate(actualDate):
    date = datetime.datetime.strptime(actualDate, '%m-%d-%Y %H:%M:%S')
    current_date = datetime.datetime.now()

    diff = relativedelta(date, current_date)

    return str(diff.days) + "d " + str(diff.hours) + "h " + str(diff.minutes) + "m " + str(diff.seconds) + "s"

while True:

    x = datetime.datetime.now()

    minute = int(x.strftime("%M"))
    seconds = int(x.strftime("%S"))

    if seconds == 0 and (minute % 10 == 0):
        # Recalculate and update title + db
        recalculate(CHANNEL_ID, VIDEO_ID)
        print("title and db updated")

        time.sleep(30)




    elif seconds == 0:
        # recalculate and update DB
        recalculate(CHANNEL_ID, VIDEO_ID)
        print("db updated")
        time.sleep(30)

