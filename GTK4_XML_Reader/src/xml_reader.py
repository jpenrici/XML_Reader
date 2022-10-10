# -*- Mode: Python3; coding: utf-8; indent-tabs-mpythoode: nil; tab-width: 4 -*-
'''
    Simple XML and SVG file reader.
'''

import os
import sys
import time

class XmlReader():

    def __init__(self, path, tags=[]):
        self.path = path
        self.tags = tags

    def load(self, path):
        text = ""
        try:
            f = open(path, 'rb')
            skip = ["\x00", "\x09", "\x0A"]
            for line in f.readlines():
                text += str("".join([(chr(x) if not chr(x) in skip else '') for x in line]))
            f.close()
            print("Load:", path)
        except IOError:
            print("Error:", path)
        return text

    def save(self, path, text):
        try:
            f = open(path, "w")
            f.write(text)
            f.close()
            print("Save:", path)
        except Exception:
            print("Error:", path)
            exit(0)

    def separate(self, text):
        txt = ""
        parts = []
        active = False
        for character in text:
            if character == '<' and not active:
                if not txt.replace(' ', '') == "":
                    parts += [txt]
                txt = character
                active = True
                continue
            if character == '>' and active:
                parts += [txt + character]
                txt = ""
                active = False
                continue
            txt += character
        if not txt == "":
            parts += [txt]

        txt = ""
        blank_spaces = False    
        quotation_marks = False
        for index in range(0, len(parts)):
            if not parts[index].startswith('<'):
                continue
            for character in parts[index]:
                if character == '"':
                    quotation_marks = not quotation_marks
                    txt += '"'
                    continue
                if character == ' ' and not quotation_marks:
                    blank_spaces = True
                    continue
                if blank_spaces and not quotation_marks:
                    txt += (' ' + character).replace(" =", "=").replace("= ", "=")
                    blank_spaces = False
                    continue
                txt += character
            parts[index] = txt
            txt = ""

        return parts

    def select(self, data, tags):
        lines = []
        for index in range(0, len(data)):
            parts = {}
            selected = False
            for tag in tags:
                if data[index].startswith("<" + tag):
                    p1 = data[index].split(' ')
                    parts['line'] = index
                    parts['tag'] = tag
                    for p in p1:
                        p2 = p.split('=')
                        if len(p2) > 1:
                            parts[p2[0]] = p2[-1]
                    selected = True
                    break
            if selected:
                lines += [parts]
        return lines

    def prepare(self):
        time_start = time.time()
        print("Select:", self.tags)

        f = self.path.strip().lower()
        if not f.endswith(".svg") and not f.endswith(".xml"):
            print("Wrong file extension!")
            return None

        text = self.load(self.path)
        if not text.startswith("<?xml"):
            print("Wrong XML declaration!")
            return None

        data = []
        if len(self.tags) > 0:
            data = self.select(self.separate(text), self.tags)
        else:
            data = self.separate(text)
        print("Runtime: {:.6f} seconds.".format(time.time() - time_start))

        return data

if __name__ == "__main__":

    def view(data):
        for i in data:
            print(i)

    xml = XmlReader("example.xml")
    svg = XmlReader("draw.svg", ["rect", "circle", "ellipse", "path", "text"])

    view(xml.prepare())
    view(svg.prepare())