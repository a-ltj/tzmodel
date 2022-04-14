#!/usr/bin/env/ python3
# -*- encoding: utf-8 -*-

from models.Line import Line


class ConnectLine(Line):
    """ 连接线类
    """

    def __init__(self, x1, x2, y1, y2):
        super().__init__(x1, x2, y1, y2)
        self.__links = []

    def setID(self, id):
        self.__id = id

    def getID(self):
        return self.__id

    def add_link(self, link):
        self.__links.append(link)

    def link_str(self):
        link_str = ''
        for link in self.__links:
            link_str += link
            link_str += ';'
        if link_str != '':
            link_str = link_str[:-1]
        return link_str
