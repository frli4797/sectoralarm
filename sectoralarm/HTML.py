# -*- coding: utf-8 -*-
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from html.parser import HTMLParser


def get_value(key, attrs):
    """ Find the key and return it's value """
    for attr in attrs:
        if attr[0] == key:
            return attr[1]


class ParseHTMLToken(HTMLParser):
    """ Parse the HTML data and return the CSRF-token """

    def __init__(self):
        self.tokens = []
        HTMLParser.__init__(self)

    def handle_endtag(self, tag):
        return

    def handle_data(self, data):
        return

    def handle_starttag(self, tag, attrs):
        if tag == 'input':
            for attr in attrs:
                if attr[0].lower() == 'name' and attr[1] == '__RequestVerificationToken':
                    self.tokens.append(get_value('value', attrs))
