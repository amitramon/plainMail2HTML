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

"""plainMail2HTML main settings module

If you install this package keeping its original structure, it should
work without modifications to the settings. However, you can always
tweak it to suit your needs.
"""

import os

# The HTML template used for creating the HTML mail part.  Of course
# it can be defined directly here, but environment variables sometimes
# allow for more flexibility.
# Modify the template to your needs.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_HTML_TEMPLATE = os.path.join(BASE_DIR, 'templates/template.html')

# A full path the the HTML template used for creating the HTML
# component. For example see the template provided with this package.
HTML_TEMPLATE = os.environ.get("PLAIN_TO_HTML_TEMPLATE", DEFAULT_HTML_TEMPLATE)

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

# Define the parset to use for parsing text into HTML. This is a
# string defining a python function. In principle you should be able
# to use any parser, although so far I only tested reStructuredText
HTML_PARSER = 'plain2html.markup.rst.restructuredtext'
