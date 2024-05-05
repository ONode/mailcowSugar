# !/usr/bin/env python
# coding: utf-8
import codecs
import datetime
import logging
import os
import json
import time
from os.path import isdir
import random
from lib.const import LocalConf


def readconf(file_name: str, required_values: list[str]) -> dict:
    """
    reading the external configuration file in json format.
    find the configuration in the cache folder or other sources
    """
    tries = 0
    config = None
    possible_folders = ["assets", "app", "config", "cache"]
    while True:
        try:
            use_folder = ""
            for e in possible_folders:
                if isdir(e) is True:
                    use_folder = e
                    break
            source_path = os.path.join(f"./{use_folder}", file_name)
            if os.path.isfile(source_path):
                try:
                    config = json.load(open(source_path, 'r'))
                except json.decoder.JSONDecodeError:
                    io = open(source_path, 'r')
                    content = io.read()
                    io.close()
                    content = remove_escape_sequences(content)
                    config = json.loads(content)
            else:
                logging.error(
                    f"configuration file is not found. {source_path} please check with the directory settings")
                exit(404)

            if isinstance(config, dict):
                missing_values = [value for value in required_values if config[value] is None]
                if len(missing_values) > 0:
                    logging.error(
                        f'The following environment values are missing in your .env: {", ".join(missing_values)}')
                    exit(405)

            return config

        except FileNotFoundError:
            print("try again.. read files")
            tries += 1
            if tries > 5:
                logging.error(f"tried {tries} times to find the file and still not found.")
                exit(404)
            continue


def remove_escape_sequences(string):
    return string.encode('utf-8').decode('unicode_escape')


class NameUtil:

    @staticmethod
    def withFix(pre: str, sub: str, number: bool):
        A = random.choice(LocalConf.FIRST_NAME_DICT).strip()
        A = A.replace("\n", "")
        B = random.choice(LocalConf.SURNAME_DICT).strip()
        B = B.replace("\n", "")
        K = str(random.randrange(111, 999, 1))
        return pre + A + B + K if number is True else "" + sub

    @staticmethod
    def init_dict():
        f1 = os.path.join(LocalConf.ASSETS_DIR, "kr_surname.txt")
        f2 = os.path.join(LocalConf.ASSETS_DIR, "firstname.txt")
        with open(f1) as ua_file:
            LocalConf.SURNAME_DICT = ua_file.readlines()
            ua_file.close()

        with open(f2) as ua_file:
            LocalConf.FIRST_NAME_DICT = ua_file.readlines()
            ua_file.close()

    @classmethod
    def get_name(cls, withNumber: bool = False):
        return cls.withFix("", "", withNumber)

    @classmethod
    def get_solname(cls, withNumber: bool = False):
        return cls.withFix("", ".sol", withNumber)

    @classmethod
    def get_ethname(cls, withNumber: bool = False):
        return cls.withFix("", ".eth", withNumber)

    @classmethod
    def get_name_simple(cls):
        return cls.withFix("", "", False)
