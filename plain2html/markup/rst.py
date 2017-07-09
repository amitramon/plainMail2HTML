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

"""A reStructuredText parser

Parse rst-markup text and convert it to HTML. cebn's hibidi code is
used to create directional-aware HTML based on the text language.

Credits: 

"""

from docutils.core import publish_parts
from docutils.writers.html4css1 import Writer
from plain2html import settings
from plain2html.core.message_utils import indent_quoted_text, load_template
from plain2html.hibidi import hibidi

def restructuredtext(text):
    """Convert rst-formatted tex into HTML"""
    
    docutils_settings = getattr(settings, "RESTRUCTUREDTEXT_FILTER_SETTINGS", {})

    # Handle any quoted text.
    fixed_text = indent_quoted_text(text)

    # Generate the HTML part.
    parts = publish_parts(source=fixed_text, writer_name="html4css1",
                          settings_overrides=docutils_settings)

    html_body = parts["html_body"]

    # Insert the body into the template.
    html = load_template(settings.HTML_TEMPLATE, html_body)

    # Process the HTML in-place and add BIDI tags based on language
    return hibidi.hibidi_unicode(html)



