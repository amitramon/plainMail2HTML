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
plainMail2HTML main settings modul.
"""

import os

# The HTML template used for creating the HTML mail part.  Of course
# it can be defined directly here, but environment variables sometimes
# allow for more flexibility.
# Modify the template to your needs.
DEFAULT_HTML_TEMPLATE = os.environ["MUTT_HTML_TEMPLATE"]

# The amount by which to indent quotes in the HTML part.
QUOTE_INDENT = ' ' * 2

# The pattern identifying quoted text.
QUOTE_PATTERN = r"^>[>\t ]*"

# Passed over to the rst parser.
RESTRUCTUREDTEXT_FILTER_SETTINGS = {
    'halt_level': 2,
    'language_code': 'en',
    'embed_stylesheet': False,  # these 2 lines prevent inserting CSS
    'stylesheet_path': ''       # code, either inline or linked.
    }

DEBUG = False

# The command to use for sending the mail. It should be the command
# your MUA (mail client) would usually use.

SENDMAIL_CMD='/usr/sbin/sendmail -oi'

# use this when debugging in command line mode to view the result on
# screen rather then actually sending it.

# SENDMAIL_CMD='cat'

# define the parset to use for parsing text into HTML This is a string
# to a python function. You may use any parser, although I tested only
# rst so far.

HTML_PARSER = 'plain2html.markup.rst.restructuredtext'
