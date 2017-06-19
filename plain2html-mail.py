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

import argparse
import sys

from plain2html import settings
from plain2html.core.sendmail import sendmail
from plain2html.core.message_processor import MessageProcessor

__usage__ = """
   cat <file> | html-mailer [options]
   html-mailer [options]
"""

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



def get_args():

    parser = argparse.ArgumentParser(
        description='Create a HTML message part for a given email message and attach it to the message.',
        usage=__usage__)
    
    parser.add_argument('-m', '--message_file', type=argparse.FileType('r'),
                        default=sys.stdin,
                        help='an email file to process.')
    
    parser.add_argument('-d', '--debug', action='store_true',
                        help='break into debugger.')

    # parser.add_argument('sendmail_args', nargs=argparse.REMAINDER,
    #                     help='possibly arguments for sendmail command.')

    return parser.parse_args()

    
def print_args(args):
    print(args)

    
def main():
    """The main function."""

    args = get_args()

    print_args(args)
    #sys.exit()
    
    try:
        if args.debug:           # a hack for development stage.
            import pdb
            pdb.set_trace()

        html_parser = get_callback(settings.HTML_PARSER)
        mp = MessageProcessor(html_parser=html_parser)

        html_msg = mp.generate_html_msg_from_file(args.message_file)

        sys.stdout.write(str(html_msg))
        
    except Exception as e:
        if settings.DEBUG:
            import traceback
            traceback.print_exc()
        else:
            print(e)
        sys.exit(1)
    else:
        sys.exit()

main()
