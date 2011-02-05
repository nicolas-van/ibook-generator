# -*- coding: utf-8 -*-
##############################################################################
#
#    Fire Wolf, Interactive Book Engine
#    Copyright (C) 2011 Nicolas Vanhoren.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import re

_split_pages_regex = re.compile(r"(\s*)(\\*)(\{\s*page\s*\:\s*([\w\.]+)\s*\})$")

def split_pages(stream):
    pages = {}
    page = None

    for line in stream:
        res = _split_pages_regex.match(line)
        if res:
            if len(res.group(2)) > 0:
                line = res.group(1) + res.group(2)[:len(res.group(2)) / 2] + res.group(3)
                pages[page] += "\n" + line
            page = res.group(4)
            pages[page] = ""
        elif not page is None:
            pages[page] += "\n" + line

    for k, v in pages.iteritems():
        pages[k] = v.strip()
    return pages


