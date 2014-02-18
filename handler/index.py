#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""
    Index Route
"""
from tornado.web import RequestHandler
from tornado_menumaker import page, index

__author__ = 'Severin Orth <severin.orth@st.ovgu.de>'
__date__ = '18.02.14 - 00:53'


@page('/', 'Index')
class Handler(RequestHandler):
    """
        Base Handler
    """

    def initialize(self, caption):
        self.caption = caption

        super().initialize()

    @index
    def get(self):
        self.render('index.tpl')