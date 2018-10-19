# -*- coding: utf-8 -*-
import urllib
import urllib.request
from urllib import error
import os
from lxml import etree
from http.client import RemoteDisconnected
import socket
from prettyprinter import pprint


def crawl():
    base_dir = os.getcwd() + '/'
    domain = input('http://www.youzifour.cc\n')
    url = domain + '/mm/baoru/index_2.html'
    page = urllib.request.urlopen(url)
    index = page.read()
    xml = etree.HTML(index)
    # 根据id为Tag_list可以得到当前页面的所有图片集入口;class为page可以拿到页码元素分析一共有多少页
    link_list = xml.xpath('//ul[@id="Tag_list"]/li/a')
    for link in link_list:
        # 读取图片集入口页
        page1 = urllib.request.urlopen(domain + link.xpath('@href')[0])
        index1 = page1.read()
        xml1 = etree.HTML(index1)

        pages = xml1.xpath('//div[@class="page"]/a/@href')
        # 拿到最后一页的链接, 分析出总页码
        # string
        last_page_url = pages[-2]
        combine = last_page_url.split('_')
        prefix = combine[0]
        total_page_num = int(combine[-1].split('.')[0])
        # 开始每一个页面的图片获取
        # 先把当前第一页的图片保存

        # 标题
        title = xml1.xpath('//div[@id="picBody"]/p/a/img/@title')[0]
        # 如果文件夹存在就当做是重复了, 跳过本次
        local_dir = base_dir + 'img/' + title
        if os.path.exists(local_dir):
            continue
        # 建立文件夹.
        os.makedirs(local_dir)

        # 图片地址
        img_src = xml1.xpath('//div[@id="picBody"]/p/a/img/@src')[0]
        # noinspection PyBroadException
        try:
            # 下载图片
            header1 = {'Referer': domain, "User-Agent": "Mozilla/5.1 (X11; Ubuntu; Linux x86_64; rv:45.139) Gecko/20100101 Firefox/45.0"}
            rq = urllib.request.Request(img_src, headers=header1)
            res = urllib.request.urlopen(rq).read()
            with open(local_dir + '/' + '1' + '.jpg', 'wb') as f:
                f.write(res)
                print('【下载成功】{0} 第{1}张图片'.format(title, 1))
        except Exception:
            print('【下载失败】{0} 第{1}张图片'.format(title, 1))

        # 开始下载第2张到最后一张图片
        for i in range(2, total_page_num + 1):
            current_url = prefix + '_' + str(i) + '.html'
            try:
                # 读取图片所在页
                page11 = urllib.request.urlopen(current_url, timeout=3)
            except (
                    RemoteDisconnected,
                    error.ContentTooShortError,
                    error.HTTPError,
                    error.URLError,
                    socket.timeout
            ) as e:
                print(e)
                return
                continue
            index11 = page11.read()
            xml11 = etree.HTML(index11)
            img_src11 = xml11.xpath('//div[@id="picBody"]/p/a/img/@src')[0]

            # 下载图片
            # noinspection PyBroadException
            try:
                # 下载图片
                rq1 = urllib.request.Request(img_src11, headers=header1)
                res1 = urllib.request.urlopen(rq1, timeout=3).read()
                with open(local_dir + '/' + str(i) + '.jpg', 'wb') as f:
                    f.write(res1)
                    print('【下载成功】{0} 第{1}张图片'.format(title, i))
            except (
                RemoteDisconnected,
                error.ContentTooShortError,
                error.HTTPError,
                error.URLError,
                socket.timeout
            ) as e:
                print(e)
                print('【下载失败】{0} 第{1}张图片'.format(title, i))
                continue

    # 进入具体的图片集页面后, 根据id为picBody可以拿到当前页面图;class为page可以拿到页码元素分析一共有多少页

    # 分析页面元素, 找出所有的图片集入口链接
    # 在图片集首页分析出所有的页面链接, 这一步要先判断是否已经建立文件夹, 并做好去重
    # 循环读取每一个链接, 并分析出主图, 下载图片保存, 注意命名编号



    # print(type(response))
    # 判断是否未创建目录
    # if not os.path.exists(path):
    #     os.makedirs(path)

    return


crawl()
