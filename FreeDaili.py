#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by master on 2017/4/7

class Daili(object):
    def __init__(self, ip, port, anonymous, types, location, speed, verify_time):
        self.ip = ip
        self.port = port
        self.anonymous = anonymous
        self.types = types
        self.location = location
        self.speed = speed
        self.verify_time = verify_time

    def __str__(self):
        print(self.ip, self.port, self.anonymous, self.types, self.location, self.speed, self.verify_time)
