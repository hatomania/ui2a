# MIT License
#
# Copyright (c) 2022 hatomania
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

import sys
import argparse
import xml.etree.ElementTree as ET

class Singleton(object):
    @classmethod
    def get_instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

class Argument(Singleton):
    def __init__(self):
        self._parser = argparse.ArgumentParser(description="Here is a description.")
        self._parser.add_argument("ui_file", help="a UI file made with Qt Designer.")
        self._parser.add_argument('--classname', help="class name of your main window (default: MainWindow)", default="MainWindow")
        #self._parser.add_argument('-o', '--output', help="")
        self._args = self._parser.parse_args()

    @classmethod
    def uifile(cls) -> str:
        return Argument.get_instance()._args.ui_file

    @classmethod
    def form_classname(cls) -> str:
        return Argument.get_instance()._args.classname

def main():
    tree = ET.parse(Argument.uifile())
    root = tree.getroot()
    elm_class = root.findall("class")
    if elm_class is None:
        print('Error: Missing "class" element.', file=sys.stderr)
        return 11
    if len(elm_class) > 1:
        print('Error: Found too many "class" elements.', file=sys.stderr)
        return 12
    ui_classname = elm_class[0].text
    elm_widget = root.findall("widget")
    if elm_widget is None:
        print('Error: Missing "widget" element.', file=sys.stderr)
        return 21
    if len(elm_widget) > 1:
        print('Error: Found too many "widget" elements.', file=sys.stderr)
        return 22
    elm_actions = elm_widget[0].findall("action")
    if elm_actions is None:
        print('Error: Missing "action" element(s).', file=sys.stderr)
        return 31

    str_connections = " <connections>\n"
    str_slots_tag = " <slots>\n"
    str_slots_decl = "public slots:\n"
    str_slots_impl = ""
    for e in elm_actions:
        aname = e.attrib["name"]
        cname = Argument.form_classname()
        str_bool = ""
        str_bool_arg = ""
        for ep in e.iter("property"):
            if ep.attrib["name"] == "checkable" and ep.find("bool").text.lower() == "true":
                str_bool = "bool"
                str_bool_arg = "bool checked"
                break
        str_connections += "  <connection>\n"
        str_connections += "   <sender>"+aname+"</sender>\n"
        str_connections += "   <signal>triggered("+str_bool+")</signal>\n"
        str_connections += "   <receiver>"+ui_classname+"</receiver>\n"
        str_connections += "   <slot>"+aname+"("+str_bool+")</slot>\n"
        str_connections += "   <hints>\n"
        str_connections += "    <hint type=\"sourcelabel\">\n"
        str_connections += "     <x>-1</x>\n"
        str_connections += "     <y>-1</y>\n"
        str_connections += "    </hint>\n"
        str_connections += "    <hint type=\"destinationlabel\">\n"
        str_connections += "     <x>0</x>\n"
        str_connections += "     <y>0</y>\n"
        str_connections += "    </hint>\n"
        str_connections += "   </hints>\n"
        str_connections += "  </connection>\n"
        #str_connections += ""
        str_slots_tag += "  <slot>"+aname+"("+str_bool+")</slot>\n"
        str_slots_decl += "  void "+aname+"("+str_bool_arg+");\n"
        str_slots_impl += "void "+cname+"::"+aname+"("+str_bool_arg+") {}\n"
    str_connections += " </connections>\n"
    str_slots_tag += " </slots>\n"
    print(str_connections, end="")
    print(str_slots_tag)
    print(str_slots_decl)
    print(str_slots_impl)
    print("Copy and paste this text to your .h, .cpp and .ui files.")

    return 0

if __name__ == "__main__":
    sys.exit(main())
