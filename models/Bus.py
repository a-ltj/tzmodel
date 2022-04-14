#!/usr/bin/env/ python3
# -*- encoding: utf-8 -*-

from models.Line import Line


class Bus(Line):
    """ 母线类
    """

    def __init__(self, x1, y1, x2, y2):
        super().__init__(x1, y1, x2, y2)

    def setID(self, id):
        self.__id = id

    def getID(self):
        return self.__id

    def setTextID(self, text_id):
        self.__text_id = text_id

    def getTextID(self):
        return self.__text_id
