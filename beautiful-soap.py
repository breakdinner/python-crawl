# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib import request
from prettyprinter import pprint


def crawl():
    req = request.Request('https://coding.imooc.com')
    rlb = request.urlopen(req, timeout=3).read()
    bs = BeautifulSoup(rlb, 'lxml')

    courses = bs.select('div.shizhan-intro-box')

    all = []
    for i in courses:
        all.append({
            'title': i.select('p.shizan-name')[0].get_text(),
            'desc': i.select('p.shizan-desc')[0].get_text(),
        })

    pprint(all)


crawl()
