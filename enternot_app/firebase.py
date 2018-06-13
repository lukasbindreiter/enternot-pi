import os
import time

from pyfcm import FCMNotification

# Minimum waiting time after sending one notification before the next
# one can be sent. Default value = 5 min
from enternot_app.pi.distance import calculate_distance

PUSH_NOTIFICATION_INTERVAL = 5 * 60

# How many meters the user needs to be away from the pi in order to
# receive notifications. Default value = 500 meters
MIN_DISTANCE_FOR_NOTIFICATIONS = 500


def get_api_key():
    try:
        from enternot_app.secret import FIREBASE_API_KEY as api_key
    except ImportError:
        api_key = os.getenv("ENTERNOT_FIREBASE_API_KEY")
    return api_key


def get_pi_location():
    try:
        from enternot_app.secret import PI_LONGITUDE as pi_lon, \
            PI_LATITUDE as pi_lat
    except ImportError:
        pi_lon = None
        pi_lat = None
    return pi_lon, pi_lat


class Firebase:
    def __init__(self):
        api_key = get_api_key()
        if api_key is not None:
            self.push_service = FCMNotification(api_key=get_api_key())
        self.last_send_time = None
        self.notifications = True

    def toggle_notifications_based_on_distance(self, lon, lat):
        distance_meters = calculate_distance(lon, lat, *get_pi_location())

        if distance_meters is None:
            return -1

        self.notifications = (distance_meters > MIN_DISTANCE_FOR_NOTIFICATIONS)
        return distance_meters

    def send_movement_push_notification(self):
        delta = time.time() - (self.last_send_time or 0)
        if delta > PUSH_NOTIFICATION_INTERVAL:
            self.last_send_time = time.time()
            self._send_push_notification(
                "movement",
                "Detected movement in front of your house!",
                "Movement detected!")

    def _send_push_notification(self, topic, message, title):
        if self.push_service is not None:
            self.push_service.notify_topic_subscribers(
                topic,
                message_body=message,
                message_title=title)
        else:
            print("Skipped sending push notification, API key not provided!")
