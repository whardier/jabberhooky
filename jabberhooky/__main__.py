#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""JabberHooky"""

import sys

import logging

import urllib2
import simplejson

import tornado.web
import tornado.ioloop
import tornado.gen
import tornado.httpclient

import sleekxmpp

# ╻ ╻┏┳┓┏━┓┏━┓╻ ╻┏━┓┏┓╻╺┳┓╻  ┏━╸┏━┓
# ┏╋┛┃┃┃┣━┛┣━┛┣━┫┣━┫┃┗┫ ┃┃┃  ┣╸ ┣┳┛
# ╹ ╹╹ ╹╹  ╹  ╹ ╹╹ ╹╹ ╹╺┻┛┗━╸┗━╸╹┗╸

class XMPPHandler(sleekxmpp.ClientXMPP):

    def __init__(self, jid, password, callback):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        self.callback = callback

        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)


    def start(self, event):
        self.send_presence()
        self.get_roster()

    def message(self, msg):
        urllib2.urlopen(self.callback, repr(msg))

# ┏┳┓┏━┓╻┏┓╻╻ ╻┏━┓┏┓╻╺┳┓╻  ┏━╸┏━┓
# ┃┃┃┣━┫┃┃┗┫┣━┫┣━┫┃┗┫ ┃┃┃  ┣╸ ┣┳┛
# ╹ ╹╹ ╹╹╹ ╹╹ ╹╹ ╹╹ ╹╺┻┛┗━╸┗━╸╹┗╸

class SendHandler(tornado.web.RequestHandler):
    def initialize(self, xmpp=None):
        self.xmpp = xmpp

    def post(self):
        print "SendHandler Called"
        self.xmpp.send_message(**simplejson.loads(self.request.body))
        self.write("OK\r\n")

# ┏━╸┏━┓╻  ╻  ┏┓ ┏━┓┏━╸╻┏ ┏━┓┏━┓┏━┓╻ ╻╻ ╻╻ ╻┏━┓┏┓╻╺┳┓╻  ┏━╸┏━┓
# ┃  ┣━┫┃  ┃  ┣┻┓┣━┫┃  ┣┻┓┣━┛┣┳┛┃ ┃┏╋┛┗┳┛┣━┫┣━┫┃┗┫ ┃┃┃  ┣╸ ┣┳┛
# ┗━╸╹ ╹┗━╸┗━╸┗━┛╹ ╹┗━╸╹ ╹╹  ╹┗╸┗━┛╹ ╹ ╹ ╹ ╹╹ ╹╹ ╹╺┻┛┗━╸┗━╸╹┗╸

class CallbackProxyHandler(tornado.web.RequestHandler):
    def initialize(self, callback=None):
        self.callback = callback
        
    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        print "CallbackProxyHandler Called"
        self.finish()
        http_client = tornado.httpclient.AsyncHTTPClient()
        response = yield tornado.gen.Task(http_client.fetch, self.callback, method='POST', body=self.request.body)

# ╺┳╸┏━╸┏━┓╺┳╸┏━╸┏━┓╻  ╻  ┏┓ ┏━┓┏━╸╻┏ ╻ ╻┏━┓┏┓╻╺┳┓╻  ┏━╸┏━┓
#  ┃ ┣╸ ┗━┓ ┃ ┃  ┣━┫┃  ┃  ┣┻┓┣━┫┃  ┣┻┓┣━┫┣━┫┃┗┫ ┃┃┃  ┣╸ ┣┳┛
#  ╹ ┗━╸┗━┛ ╹ ┗━╸╹ ╹┗━╸┗━╸┗━┛╹ ╹┗━╸╹ ╹╹ ╹╹ ╹╹ ╹╺┻┛┗━╸┗━╸╹┗╸

class TestCallbackHandler(tornado.web.RequestHandler):
    def post(self):
        print "Test Callback Hit", self.request.body

# ┏━┓╻ ╻┏┓╻
# ┣┳┛┃ ┃┃┗┫
# ╹┗╸┗━┛╹ ╹

def run():

    tornado.httpclient.AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")

    xmpp = XMPPHandler('popcorn@bigboote.microcom.tv', 'popcorn', 'http://localhost:8080/callback')
    xmpp.register_plugin('xep_0030')

    if xmpp.connect():
        xmpp.process(block=False)

    application = tornado.web.Application([
            tornado.web.URLSpec(r"/send", SendHandler, {'xmpp': xmpp}),
            tornado.web.URLSpec(r"/callback", CallbackProxyHandler, {'callback': "http://localhost:8080/testcallback"}),
            tornado.web.URLSpec(r"/testcallback", TestCallbackHandler),
        ],
        )

    application.listen(8080)

    ioloop = tornado.ioloop.IOLoop.instance()

    try:
        ioloop.start()
    except KeyboardInterrupt:
        print "I'm out"
        xmpp.disconnect()    

if __name__ == "__main__":
    run()
