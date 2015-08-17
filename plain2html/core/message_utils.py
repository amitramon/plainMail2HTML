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
A bunch of utilities to process email messages.
"""

import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.feedparser import FeedParser
from plain2html import settings

# list of email headers that shouldn't
# be copied when cloning a new message
# from a different one.
header_blacklist = ('content-disposition', 'content-type',
                    'mime-version', 'content-transfer-encoding')

def is_header_okay(header):
    return not header.lower() in header_blacklist


def convert_text_to_alternative(msg):
    # Create message container - the correct MIME type is multipart/alternative.
    new_msg = MIMEMultipart('alternative')
    new_msg.set_unixfrom(msg.get_unixfrom())
    new_msg.set_charset(msg.get_charset())
    
    for key in msg.keys():
        if is_header_okay(key):
            new_msg.add_header(key, msg[key])

    return new_msg


def load_message(fp):
    """Load message from a file handle.

    Reads data from a file handler and parse it
    to a message object.
    """
    parser = FeedParser()
    for line in fp.readlines():
        parser.feed(line)
    
    return parser.close()
        

def load_template(template, body):
    fp = open(template)
    template = fp.read()
    fp.close()
    return template % {'body': body}



DEFAULT_QUOTE_INDENT = ' ' * 4
DEFAULT_QUOTE_PATTERN = r"^>[>\t ]*"

# TODO: change code to always add > when indenting. Oops, not
# a good idea... if using HTML paragraphs, the > marks will not
# stay at the beginning of line.

def indent_quoted_text(text):
    # matching till last space and removing match causes loosing
    # previous indentation. however, without it, indentation can become
    # uneven, causing rst to complain. this means that text which is
    # intentionally indented looses its indentation. 
    #qre = re.compile(r"^[>\t ]*")
    prev_quote_level = 0
    new_lines = []
    lines = text.splitlines(True) # keep end-of-line chars
    quote_indent = getattr(settings, "QUOTE_INDENT", DEFAULT_QUOTE_INDENT)
    quote_pattern = getattr(settings, "QUOTE_PATTERN", DEFAULT_QUOTE_PATTERN)

    qre = re.compile(quote_pattern)

    # go over lines, replace quote marks by indentation,
    # add blank lines between different indentation levels.
    new_lines = []
    for line in lines:
        match_obj = qre.search(line)
        if not match_obj:
            quote_level = 0
            new_line = line
        else:
            match = match_obj.group(0)
            quote_level = match.count('>')
            new_line = line.replace(match, quote_indent * quote_level, 1)

        if quote_level != prev_quote_level:
            new_lines.append('\n')
            prev_quote_level = quote_level
            
        new_lines.append(new_line)

    return ''.join(new_lines)
