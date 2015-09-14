#!/usr/bin/env python

# Author: Amit Ramon <amitrm@users.sourceforge.net>

# This file is part of plainMail2HTML.

# plainMail2HTML is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

# plainMail2HTML is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with plainMail2HTML.  If not, see
# <http://www.gnu.org/licenses/>.

"""
plainMail2HTML is a tool that creates and attaches a text/html part to
a text/plain email message. It then passes the message over to an external
mail-sending utility (e.g., sendmail).

plainMail2HTML was written with the Mutt email client (see
<http://www.mutt.org> in mind, in order to allow sending email
messages in HTML format.

For Mutt, the typical usage is to define the following definition in
Mutt's configuration file:

sendmail="plain2html-mail.py -- $@"

See also the settings file for important plainMail2HTML configuration.

"""

import getopt
import sys

from plain2html import settings
from plain2html.core.sendmail import sendmail
from plain2html.core.message_processor import MessageProcessor

__usage__ = """
Usage: cat <file> | html-mailer [options]
       html-mailer [options]
Create and attach a HTML message to a given email message,
then send it.

Options:
  -h, --help               print brief usage message.
  -m, --message-file       an email file to process.
  -q, --quote-prefix       the prefix used to quote text when replying.
  -d, --debug              break into debugger.
"""

def usage():
    print __usage__

_short_opt = 'hdm:q:'
_long_opt = ('help', 'message-file=', 'quote-prefix=', 'debug')

def get_callback(callback_str):
    """Return a function reference for the function name.

    callback_str: a string representing the function.

    """
    # This is a quick-n-dirty patch. Need especially better error
    # handling.
    dot = callback_str.rindex('.')
    mod_name, func_name = callback_str[:dot], callback_str[dot+1:]
    __import__(mod_name)
    # import pdb;pdb.set_trace()
    return getattr(sys.modules[mod_name], func_name)

def main():
    """The main function."""

    try:
        opts, sendmail_args = getopt.getopt(sys.argv[1:], _short_opt, _long_opt)
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    
    message_file = None
    verbose = False
    quote_prefix = getattr(settings, 'QUOTE_PREFIX', '>')
    html_direction_rtl = False
    dbg_break = False

    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-m", "--message-file"):
            message_file = a
        elif o in ("-q", "--quote-prefix"):
            quote_prefix = a
        elif o in ("-r", "--rtl"):
            html_direction_rtl = True
        elif o in ("-d", "--debug"):
            dbg_break = True
        else:
            assert False, "unhandled option"
 
    try:
        if dbg_break:           # a hack for development stage.
            import pdb
            pdb.set_trace()

        html_parser = get_callback(settings.HTML_PARSER)
        mp = MessageProcessor(html_parser=html_parser)

        fp = open(message_file) if message_file else sys.stdin
        html_msg = mp.generate_html_msg_from_file(fp)
        # sendmail(html_msg, sendmail_args)
        sys.stdout.write(str(html_msg))
        
    except Exception, e:
        if settings.DEBUG:
            import traceback
            traceback.print_exc()
        else:
            print e
        sys.exit(1)
    else:
        sys.exit()

main()
