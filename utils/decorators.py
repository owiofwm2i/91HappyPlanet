# -*- coding: utf-8 -*-
from functools import wraps
from utils.sqlite import Database

db = Database()


def insertDataToDb(func):

    @wraps(func)
    def decorator(self, url):
        fileName, urls, files = func(self, url)

    return decorator

