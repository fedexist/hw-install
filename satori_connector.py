from __future__ import print_function

import threading

from satori.rtm.client import make_client, SubscriptionMode

channel = "transportation"
endpoint = "wss://open-data.api.satori.com"
appkey = "8698EC0C7f87BB5Dc01526F0Ecd2bBFc"


def main():
    with make_client(
            endpoint=endpoint, appkey=appkey) as client:

        print('Connected!')
        
        mailbox = []
        got_message_event = threading.Event()

        class SubscriptionObserver(object):
            def on_subscription_data(self, data):
                for in_message in data['messages']:
                    mailbox.append(in_message)
                got_message_event.set()
        subscription_observer = SubscriptionObserver()
        client.subscribe(
            channel,
            SubscriptionMode.SIMPLE,
            subscription_observer)
        
        while got_message_event.wait(10):
            if len(mailbox) != 0:
                for i in range(len(mailbox)):
                    print('Got message {0} "{1}"'.format(str(i), mailbox[i]))
                del mailbox[:]


if __name__ == '__main__':
    main()
