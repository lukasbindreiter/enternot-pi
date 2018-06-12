import os
import time

from pyfcm import FCMNotification

PUSH_NOTIFICATION_INTERVAL = 5 * 60  # Limit to one push notification every 5min


def get_api_key():
    try:
        from enternot_app.secret import FIREBASE_API_KEY as api_key
    except ImportError:
        api_key = os.getenv("ENTERNOT_FIREBASE_API_KEY")
    return api_key


class Firebase:
    def __init__(self):
        api_key = get_api_key()
        if api_key is not None:
            self.push_service = FCMNotification(api_key=get_api_key())
        self.last_send_time = None
        self.notifications = True

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
