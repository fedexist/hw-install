from __future__ import print_function

import threading
import json

from satori.rtm.client import make_client, SubscriptionMode

channel = "transportation"
endpoint = "wss://open-data.api.satori.com"
appkey = "8698EC0C7f87BB5Dc01526F0Ecd2bBFc"


def main():
    with make_client(
            endpoint=endpoint, appkey=appkey) as client:
        
        mailbox = []
        got_message_event = threading.Event()

        class SubscriptionObserver(object):
            def on_subscription_data(self, data):
                for in_message in data['messages']:
                    mailbox.append(json.dumps(in_message))
                got_message_event.set()
        subscription_observer = SubscriptionObserver()
        client.subscribe(
            channel,
            SubscriptionMode.SIMPLE,
            subscription_observer)
        
        while got_message_event.wait(10):
            if len(mailbox) != 0:
                print(str(mailbox).replace("'", ""))
                del mailbox[:]


if __name__ == '__main__':
    main()
