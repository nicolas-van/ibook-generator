#!/usr/bin/env python
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

from creoleparser.dialects import create_dialect, creole10_base, creole11_base
from creoleparser.core import Parser
from optparse import OptionParser
import string
from page_splitter import split_pages

def wiki_parse(content, wiki_links_path_func):
    wiki_parser = Parser(dialect=create_dialect(creole11_base, wiki_links_path_func=wiki_links_path_func))
    return wiki_parser(content)
 
_DEFAULT_TEMPLATE = """
<html>
    <head/>
    <body>
        ${content}    
    </body>
</html>
"""


if __name__ == "__main__":
    usage = "usage: %prog [options] INPUT OUTPUT_PREFIX [TEMPLATE]"
    parser = OptionParser(usage=usage, version="%prog 1.0")

    (options, args) = parser.parse_args()

    if not len(args) in [2, 3]:
        parser.print_help()
        print "incorrect number of arguments"
        exit(-1)

    input = args[0]
    output_prefix = args[1]
    template = args[2] if len(args) > 2 else None
    
    input_file = open(input)
    pages = split_pages(input_file)
    input_file.close()

    if template:
        temp = open(template)
        template_content = string.Template(temp.read())
        temp.close()
    else:
        template_content = string.Template(_DEFAULT_TEMPLATE)

    def link(name):
        return output_prefix.split("/")[-1] + "-" + name + ".html"

    for k, v in pages.iteritems():
        output = open(output_prefix + "-" + k + ".html", "w")
        output.write(template_content.substitute({"content": wiki_parse(v, link)}))
        output.close()

