#!/usr/bin/env python3

__author__ = ['[Blazz3]']
__date__ = '16.04.2018'

import requests
import time
import re
from bs4 import BeautifulSoup
from random import randrange, uniform
import urllib.request,urllib.parse,urllib.error

REG = re.compile("(\w.+)(\/user\/register)$")
REG2 = re.compile("(Drupal)\s(7\.(5[8-9]|[6-9][0-9]))|(Drupal)\s(8\.5\.[1-9])|(Drupal)\s(8\.[6-9]\.[0-9])|(Drupal)\s([4-6]\.*[0-9]*\.*[0-9]*)")
USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

def fetch_results(search_term, number_results, language_code, randi):
    assert isinstance(search_term, str), 'Search term must be a string'
    assert isinstance(number_results, int), 'Number of results must be an integer'
    escaped_search_term = search_term.replace(' ', '+')

    google_url = 'https://www.google.com/search?q={}&num={}&hl={}&start={}'.format(escaped_search_term, number_results, language_code, randi)
    response = requests.get(google_url, headers=USER_AGENT)
    response.raise_for_status()

    return search_term, response.text

def parse_results(html, keyword):
    
    soup = BeautifulSoup(html, 'lxml')
    found_results = []
    result_block = soup.find_all('cite',string=re.compile("user/register$"))
    for result in result_block:
        found_results.append(result.text)
    return found_results

def scrape_google(search_term, number_results, language_code, randi):
    try:
        keyword, html = fetch_results(search_term, number_results, language_code, randi)
        results = parse_results(html, keyword)
        return results
    except AssertionError:
        raise Exception("Argmentos incorrectos parseados a la funcion.")
    except requests.HTTPError:
        raise Exception("Parece que has sido bloqueado por Google.")
    except requests.RequestException:
        raise Exception("Parece que hay un error en tu conexion a Internet.")
    
if __name__ == '__main__':
    print ('###################################')
    print ('# PoC CVE-2018-7600')
    print ('###################################\n')
    dork = ['intext:"Powered by Drupal" inurl:"/user/register/"']
    data = []
    irand = randrange(0, 100)
    for keyword in dork:
        try:
            results = scrape_google(keyword, 10, "es-419", irand)
            for result in results:
                data.append(result)
        except Exception as e:
            print(e)
        finally:
            time.sleep(1)
    for d in data:
        ''' for d in data: print(d.replace("user/register", "CHANGELOG.txt"))'''
        d = d.replace("http://","")
        d = d.replace("https://","")
        d = d.replace("?q=","")
        d = d.replace("user/register", "CHANGELOG.txt")
        d = d.replace("\n", "")
        d = "http://" + d + " "
        fn = True
        try:
            response = urllib.request.urlopen(d)
        except:
            print (d + " Error!")
        else:
            lines = response.readlines()
            rua = d + lines[1].decode('utf-8')
            rua = d.replace("\n", "")
            if re.match(REG2,lines[1].decode('utf-8')):
                print (rua + " No Vulnerable x_x")
            else:
                print (rua + " Vulnerable!")