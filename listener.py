import time

from pprint import pformat
import undetected_chromedriver as uc


class Custom_UC(uc.Chrome):
    request_id = None
    listner_url = None

    def RWBS_callback(self, message):
        url = message['params']['request']['url']
        request_id = message['params']['requestId']
        if url == self.listner_url:
            # смотри структуру
            # print(pformat(message))
            self.request_id = request_id

    def LF_callback(self, message):
        request_id = message['params']['requestId']
        if self.request_id == request_id:
            # смотри структуру
            # print(pformat(message))
            args = {'requestId': request_id}
            data = driver.execute_cdp_cmd('Network.getResponseBody', args)
            print(pformat(data))
            self.request_id = None


driver = Custom_UC(enable_cdp_events=True)
# прослушиваемый url
driver.listner_url = 'https://whoer.net/v2/geoip2-city'
# for more inspiration checkout the link below
# https://chromedevtools.github.io/devtools-protocol/1-3/Network/
driver.add_cdp_listener('Network.requestWillBeSent', driver.RWBS_callback)
driver.add_cdp_listener('Network.loadingFinished', driver.LF_callback)

driver.get('https://whoer.net/')
time.sleep(20)
