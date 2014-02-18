#!/usr/bin/python3.3
# -*- coding: utf-8 -*-
"""
    
"""
from _socket import gethostname
from urllib.parse import urljoin

from tornado.ioloop import IOLoop
from tornado.options import options, define
from tornado.web import Application
from tornado_menumaker import routes

__author__ = 'Severin Orth <severin.orth@st.ovgu.de>'
__date__ = '24.03.13'

define('template_path', 'templates')
define('static_path', 'static')

define('port', 4010, help="Port of application")
define('host', help="Bind interface of application")


class BaseApplication(Application):
    """
        Base Application
    """

    def __init__(self, *args, **kwargs):
        kwargs.update(options.items())
        kwargs.setdefault('handlers', []).extend(routes())

        super().__init__(*args, **kwargs)

    @property
    def port(self):
        """
            Port of application
        """
        return "port" in self.settings and self.settings["port"] or options["port"]

    @property
    def host(self):
        """
            Host of application
        """
        return "host" in self.settings and self.settings["host"] or None

    def listen(self, **kwargs):
        """
            Register the Application to a port/address
        """

        # xheaders in settings?
        kwargs['xheaders'] = kwargs.get('xheaders', self.settings.get('xheaders', False))

        # Check for host setting
        if not self.host:
            realaddress = urljoin('http://%s:%s' % (gethostname().split(".")[0], self.port), '.')
            super().listen(port=self.port, **kwargs)
        else:
            realaddress = urljoin('http://%s:%s' % (self.host, self.port), '.')
            super().listen(port=self.port, address=self.host, **kwargs)

        # Return connected interface
        return realaddress

    @staticmethod
    def start():
        """
            Start the IO Loop
        """
        try:
            IOLoop.instance().start()
        except KeyboardInterrupt:
            pass

