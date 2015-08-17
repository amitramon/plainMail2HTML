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
A reStructuredText parser.
"""

from docutils.core import publish_parts
from docutils.writers.html4css1 import Writer
from plain2html import settings
from plain2html.core.message_utils import indent_quoted_text, load_template
from plain2html.hibidi import hibidi

def restructuredtext(text):
    docutils_settings = getattr(settings, "RESTRUCTUREDTEXT_FILTER_SETTINGS", {})

    # Handle any quoted text.
    fixed_text = indent_quoted_text(text)

    # Generate the HTML part.
    parts = publish_parts(source=fixed_text, writer_name="html4css1",
                          settings_overrides=docutils_settings)

    html_body = parts["html_body"].encode('utf-8')

    # Insert the body into the template.
    html = load_template(settings.DEFAULT_HTML_TEMPLATE, html_body)

    return hibidi.hibidi_str(html, encoding='utf-8')



