# plainMail2HTML - Convert a text/plain Email to plain+HTML Email.
#
# Copyright (C) 2016 Amit Ramon <amit.ramon@riseup.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""plainMail2HTML Email message utilities

Utilities for processing Email messages.
"""

import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from plain2html import settings

# List of email headers that shouldn't be copied when cloning a new
# multipart/alternative message from at existing text/plain one.
header_blacklist = ('content-type', 'mime-version',
                    'content-transfer-encoding')

def is_header_okay(header):
    """Test that the header is allowed"""

    return not header.lower() in header_blacklist


def convert_text_to_alternative(msg):
    """Convert Email message type to multipart/alternative"""
    
    # Create message container - the correct MIME type is
    # multipart/alternative.
    new_msg = MIMEMultipart('alternative')
    
    for key in list(msg.keys()):
        if is_header_okay(key):
            new_msg.add_header(key, msg[key])

    return new_msg

def clone_header(header, msg_src, msg_dest):
    """ Clone Email header"""
    
    value = msg_src[header]
    if value is None:
        return

    del msg_dest[header]
    msg_dest[header] = value


def load_template(template, body):
    """Combine message body with a template"""
    
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
    """Convert 'old-style' Email quoted text to indented text"""

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
