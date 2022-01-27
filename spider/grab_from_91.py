#!/usr/bin/env python3

import logging
import sys
import subprocess as sp
import requests as req
from pyquery import PyQuery as pq

user_agent = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}

target_url = ''


def _config_logging(file_name: str, console_level: int = logging.INFO, file_level: int = logging.DEBUG):
    log_format = '%(asctime)s [%(levelname)s] %(module)s.%(lineno)d %(name)s:\t%(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'

    file_handler = logging.FileHandler(file_name, mode='a', encoding="utf-8")
    file_handler.setFormatter(logging.Formatter(log_format, datefmt=date_format))
    file_handler.setLevel(file_level)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(log_format, datefmt=date_format))
    console_handler.setLevel(console_level)

    logging.basicConfig(level=min(console_level, file_level), handlers=[file_handler, console_handler], )


def _run_command(command):
    res = sp.run(command, shell=True, stdout=sp.PIPE, stderr=sp.PIPE, encoding="utf-8")
    if res.returncode == 0:
        logging.info(res.stdout)
        return True
    else:
        logging.error(res.stderr)
        return False


if __name__ == '__main__':
    _config_logging('grab.log')
    logging.debug("debug")
    logging.info("info")
    logging.warning("warning")
    logging.critical("critical")
