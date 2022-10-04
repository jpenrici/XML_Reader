# -*- Mode: Python3; coding: utf-8; indent-tabs-mpythoode: nil; tab-width: 4 -*-
'''
    Simple XML and SVG file reader.
'''

import os
import sys
import time


def load(filename):

    text = ""
    try:
        f = open(filename, 'rb')
        skip = ["\x00", "\x09", "\x0A"]
        for line in f.readlines():
            text += str("".join([(chr(x) if not chr(x) in skip else '') for x in line]))
        f.close()
        print("Load:", filename)
    except IOError:
        print("Error:", filename)
    return text


def save(filename, text):

    try:
        f = open(filename, "w")
        f.write(text)
        f.close()
        print("Save:", filename)
    except Exception:
        print("Error:", filename)
        exit(0)


def separate(text):

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


def select(data, tags):

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


def prepare(filename, tags=[]):

    time_start = time.time()

    f = filename.strip().lower()
    if not f.endswith(".svg") and not f.endswith(".xml"):
        print("Wrong file extension!")
        exit(0)

    text = load(filename)
    if not text.startswith("<?xml"):
        print("Wrong XML declaration!")
        exit(0)

    data = []
    if len(tags) > 0:
        print("Select:", tags)
        data = select(separate(text), tags)
    else:
        data = separate(text)
    
    print("Runtime: {:.6f} seconds.".format(time.time() - time_start))
    # print(data)

    return data


def svg(filename):
    TAGS = ["rect", "circle", "ellipse", "path", "text"]
    data = prepare(filename, TAGS)
    for i in data:
        print(i)


def basic(filename):
    data = prepare(filename)
    for i in data:
        print(i)


if __name__ == "__main__":

    basic("example.xml")
    svg("draw.svg")