from __future__ import print_function

import threading
import json

from satori.rtm.client import make_client, SubscriptionMode

channel = "air-traffic"
endpoint = "wss://open-data.api.satori.com"
appkey = "E3BEf135eA53D785B647c3bC8FfcA506"


def main():
    with make_client(
            endpoint=endpoint, appkey=appkey) as client:
        
        mailbox = []
        got_message_event = threading.Event()

        class SubscriptionObserver(object):
            def on_subscription_data(self, data):
                for in_message in data['messages']:
                    if all(len(str(x)) > 0 for x in in_message.values()):
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
