#!/usr/bin/python3.3
# -*- coding: utf-8 -*-
"""

"""
import inspect
import os
import site
import sys

__author__ = 'Severin Orth <severin.orth@st.ovgu.de>'
__date__ = '24.03.13'

# Ensure Python 3
if sys.hexversion < 0x03030000:
    raise SystemError("Not started with minimum Python 3.3")

# Ensure Packages
from pkg_resources import require

require(open('requirements.txt').readlines())

# Add Apis
for api in next(os.walk(os.path.join(os.path.dirname(__file__), "api")))[1]:
    site.addsitedir(os.path.join(os.path.dirname(__file__), "api", api))

# Main Program
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int,
                        help='Overwrite DEFAULT_PORT of application')
    parser.add_argument('-b', '--daemonize', action="store_true", default=False,
                        help='Daemonize application')
    sparser = parser.add_subparsers()

    import application, handler

    # Load applications
    for name in dir(application):
        cls = getattr(application, name)
        if inspect.isclass(cls):

            # Add Parser
            aparser = sparser.add_parser(name)
            aparser.set_defaults(cls=cls, name=cls.__name__)

    # Load all handler (-> will make tornado_menuroute active)
    for name in dir(handler):
        cls = getattr(handler, name)
        if inspect.isclass(cls):
            pass

    # Parse Arguments
    args = parser.parse_args()
    if not hasattr(args, 'cls'):
        parser.print_usage()
        exit(1)

    if args.daemonize:
        import daemon
        import daemon.pidlockfile

        # Creating pid file
        pidfile = daemon.pidlockfile.PIDLockFile('tornado.%s.pid' % args.name.lower())

        # Creating Context
        log = open('tornado.%s.log' % args.name.lower(), 'a+')
        ctx = daemon.DaemonContext(stdout=log, stderr=log, working_directory='.')
        ctx.open()

    # Parse options
    import tornado.options
    tornado.options.parse_config_file("config/tornado.conf")

    instance = args.cls()
    if args.port:
        instance.port = args.port

    # Listen to Port and Start IOLoop
    print(instance.listen())
    instance.start()

