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
The sendmail module defines the sendmail() function that sends an
email message using a command defined in the settings file.
"""

from subprocess import Popen, PIPE, STDOUT
from plain2html import settings


def sendmail(msg, extra_args=None):
    """Send the mail in msg."""

    args = settings.SENDMAIL_CMD.split(' ')
    if extra_args: 
        args.extend(extra_args)

    send_mail = Popen(args, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    stdoutdata, stderrdata = send_mail.communicate(input=msg.as_string())
    
    if send_mail.returncode:
        msg = 'sendmail: error %d. %s' % \
            (send_mail.returncode, stdoutdata if stdoutdata else '')
        raise Exception, msg

    # This occurs either if there is an error, or the sendmail command
    # is defined as ``cat`` or in a similar way for debbuging purposes.
    if stdoutdata:
        print "Command output"
        print "=============="
        print stdoutdata
