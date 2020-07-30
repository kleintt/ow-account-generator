# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 19:24:27 2020

@author: Yongyao SUN
"""


import random
import time
import names
import string
import cloudscraper

def loadProxyUserPass(filename):
    proxyList = []
    with open(filename + '.txt') as f:
        file_content = f.read()
    file_rows = file_content.split('\n')
    for i in range(0, len(file_rows)):
        if ':' in file_rows[i]:
            tmp = file_rows[i]
            tmp = tmp.split(':')
            proxies = {'http': 'http://' + tmp[2] + ':' + tmp[3] + '@' + tmp[0] + ':' + tmp[1] + '/',
                       'https': 'http://' + tmp[2] + ':' + tmp[3] + '@' + tmp[0] + ':' + tmp[1] + '/'}
            proxyList.append(proxies)
    return proxyList 


def loadProxyIpAuth(filename):
    proxyList = []
    with open(filename + '.txt') as f:
        file_content = f.read()
    tmp = file_content.split('\n')
    for n in range(0, len(tmp)):
        if ':' in tmp[n]:
            temp = tmp[n]
            proxies = {'http': 'http://' + temp,  'https': 'http://' + temp}
            proxyList.append(proxies)
    return proxyList 

def regist(name, ran_num, domain, pw, captcha_api, proxyList):
    email = str(name)+str(ran_num)+str(domain)
    email = email.replace(' ', '')
    ua = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    s = cloudscraper.create_scraper(browser={'custom': ua}, interpreter='nodejs',
                                    captcha={'provider': '2captcha', 'api_key': captcha_api})

    try:
        if bool(proxyList) == True:
            s.proxies = random.choice(proxyList)
        headers_regist = {
                'accept': 'application/json, text/plain, */*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-GB',
                'content-type': 'application/json',
                'dnt': '1',
                'ff-country': 'DE',
                'ff-currency': 'EUR',
                'origin': 'https://www.off---white.com',
                'referer': 'https://www.off---white.com/',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'x-newrelic-id': 'VQUCV1ZUGwIFVlBRDgcA'
        }
        data = {
                'countryCode': "DE",
                'email': email,
                'name': names.get_full_name(),
                'password': pw,
                'receiveNewsletters': 'false',
                'username': email
                }
        regist_api = 'https://www.off---white.com/api/legacy/v1/account/register'
        r = s.post(regist_api, headers=headers_regist, json=data, timeout=5, allow_redirects=False)
        if r.status_code ==200:
            print(str(email)+' Successfully registed')
            acc = str(email)+':'+str(pw)
            file = open('ow_acc.txt', 'a')
            file.write(str(acc.replace('\'', '')))
            file.write("\n")
            file.close()
        else:
            print(r.status_code)
            print(str(email)+' Failed')
    except Exception as e:
        print(str(email)+' failed')
        print(f"Reason: {e}")

def regist_real_email(email_reg,pw, captcha_api, proxyList):
    ua = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    s = cloudscraper.create_scraper(browser={'custom': ua}, interpreter='nodejs',
                                    captcha={'provider': '2captcha', 'api_key': captcha_api})

    try:
        if bool(proxyList) == True:
            s.proxies = random.choice(proxyList)
        headers_regist = {
            'authority': 'www.off---white.com',
            'method': 'POST',
            'path': '/api/legacy/v1/account/register',
            'scheme': 'https',
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br',
            'content-type': 'application/json',
            'dnt': '1',
            'ff-country': 'DE',
            'ff-currency': 'EUR',
            'origin': 'https://www.off---white.com',
            'referer': 'https://www.off---white.com/',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-dest': 'empty',
            'x-newrelic-id': 'VQUCV1ZUGwIFVlBRDgcA'
        }
        data = {
                'countryCode': "DE",
                'email': email_reg,
                'name': names.get_full_name(),
                'password': pw,
                'receiveNewsletters': 'false',
                'username': email_reg
                }
        regist_api = 'https://www.off---white.com/api/legacy/v1/account/register'
        r = s.post(regist_api, headers=headers_regist, json=data, timeout=5, allow_redirects=False)
        if r.status_code == 200:
            print(str(email_reg)+' Successfully registed')
            acc = str(email_reg)+':'+str(pw)
            file = open('ow_acc.txt', 'a')
            file.write(str(acc.replace('\'', '')))
            file.write("\n")
            file.close()
        else:
            print(r.status_code)
            print(str(email) + ' Failed')
    except Exception as e:
        print(str(email_reg)+' failed')
        print(f"Reason: {e}")

if __name__ == "__main__":
    proxyList = []
    proxyIndex = 0
    try:
        proxyList =  loadProxyUserPass('proxies')
    except:
        proxyList =  loadProxyIpAuth('proxies')

    totalproxies = len(proxyList)
    if int(totalproxies) == 0:
        print('Running localhost!')
    else:
        print('Loaded %s proxies!' % totalproxies)
    mode = int(input('Mode 1: catchall    Mode 2: real email  '))
    with open('2captcha.txt') as f:
        captcha_api = f.read()
    if mode == 1:
        domain = input("Catchall domain(with@) : ")
        entryCount = int(input("Amount : "))
        pw = input('Password: ')
        for i in range(entryCount):
            name = names.get_full_name()
            ran_num = ''.join(random.sample(string.digits, 6))
            regist(name, ran_num, domain, pw, captcha_api, proxyList)
            time.sleep(1)
    elif mode == 2:
        with open('email.txt') as f:
            file_content = f.read()
        email = file_content.split('\n')
        for i in range(len(email)):
            pw = ''.join(random.sample(string.ascii_letters + string.digits, 10))
            email_reg = email[i]
            regist_real_email(email_reg, pw, captcha_api, proxyList)
            time.sleep(1)
