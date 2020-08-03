__author__ = 'joesacher'
# Copyright (c) 2020 John Price <john.price@digamesystems.com>
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v1.0
# and Eclipse Distribution License v1.0 which accompany this distribution.
#
# The Eclipse Public License is available at
#    https://eclipse.org/org/documents/epl-v10.php.
# and the Eclipse Distribution License is available at
#   https://eclipse.org/org/documents/edl-v10.php.
#
# Contributors:
#    John Price - committer
#    Joe Sacher - initial implementation  https://github.com/sacherjj/python-AlienRFID
#    And Others.


import datetime as dt


class AlienTag(object):

    def __init__(self, taglist_entry):
        self.disc = 0
        self.last = 0
        self.last_last = 0
        self.id = 0
        self.ant = 0
        self.count = 0
        self.proto = 0
        self.rssi = 0
        self.freq = 0
#        self.speed = 0
#        self.speed_smooth = 0
#        self.speed_last = 0
#        self.pos_smooth = 0
#        self.pos_last = 0
#        self.pos_min = 0
        self.create(taglist_entry)

    def __str__(self):
        return self.id

    def __gt__(self, other):
        return self.id > other.id

    def create(self, taglist_entry):
        """
        Try to parse a taglist entry into a set of Tag object variables.
        Uses a simple mapping from Alien 'text' format:
         Tag:0102 0304 0506 0708 0900 0A0B, Disc:2008/10/28 10:49:35, Last:2008/10/28 10:49:35, Count:1, Ant:3, Proto:2
        *rssi* and *speed* attributes are not included in the default text format.
        In order to have them parsed correctly the _TagListFormat_ must be set to _custom_ and
        the _TagListCustomFormat_ fields must be separated by the following text tokens:
         'tag:', 'disc:', 'last:', 'count:', 'ant:', 'proto:', 'speed:', 'rssi:'
        For example:
         @rdr.taglistcustomformat("Tag:%i, Disc:${DATE1} ${TIME1}, Last:${DATE2} ${TIME2}, Count:${COUNT}, Ant:${TX}, Proto:${PROTO#}, Speed:${SPEED}, rssi:${RSSI})"
         @rdr.taglistformat("custom")
        """
        self.id = ""
        if taglist_entry == "(No Tags)":
            return
        tagline = taglist_entry.split('\r\n')[0]
        tagbits = {}
        for keyval in tagline.split(", "):
            key, val = keyval.split(":", 1)
            # TODO: Raise Error on Bad Key Val parse
            tagbits[key.lower()] = val

        self.id = tagbits.get('tag', 'NO TAG ID')
        self.ant = tagbits.get('ant', 0)
        self.count = tagbits.get('count', 0)
        self.disc = tagbits.get('disc', 0)
        self.last = tagbits.get('last', 0)
        # TODO: Convert self.last into datetime
        self.last_last = self.last
        self.proto = tagbits.get('proto', 0)
        self.rssi = tagbits.get('rssi', 0)
        self.freq = tagbits.get('freq', 0)
        self.speed = tagbits.get('speed', 0)

    def update(self, new_tag):
        self.last = new_tag.last
        self.count += new_tag.count
        self.last_last = self.last