import httpx
from selectolax.parser import HTMLParser
from dataclasses import dataclass
from random import choice
import csv
import os
import json

@dataclass
class Job:
    title: str
    company_name: str
    company_website: str
    company_linkedin: str

@dataclass
class SSS:
    useragent: str
    proxies: list[str]
    def fetch(self, url):
        selproxy = choice(self.proxies)
        proxy = {
            "all://": f"http://{selproxy}"
        }

        header = {
            "user-agent": self.useragent
        }

        print(proxy)
        with httpx.Client(proxies=proxy, headers=header) as client:
            response = client.get(url)
        return response.text

    def parse(self, html):
        tree = HTMLParser(html)
        parent = tree.css('div[data-resultlist-offers-numbers] > div > article')
        company_names = list()
        for child in parent:
            company_name = child.css_first('a[data-at="job-item-company-name"]')
            company_names.append(company_name)
        return company_names
    def to_csv(self, data, filename, headers):
        file_exists = os.path.isfile(filename)

        with open(filename, 'a', encoding='utf-16') as f:
            writer = csv.DictWriter(f, delimiter=',', lineterminator='\n', fieldnames=headers)
            if not file_exists:
                writer.writeheader()
            writer.writerows(data)

    def list_to_json(self, data, filename):
        with open(filename, 'w') as f:
            json.dump(data, f)

    def pagination(self):
        endofpage = False
        of = 25
        while not endofpage:
            trials = 0
            while trials <= 3:
                try:
                    url = f'https://www.stepstone.de/5/ergebnisliste.html?action=facet_selected%3bcategories%3b2003000&fu=2003000&of={of}'
                    html = self.fetch(url)
                    break
                except Exception as e:
                    print(e)
                    trials += 1
            try:
                company_name = self.parser(html)
            except Exception as e:
                print(e)
                endofpage = True
            self.list_to_json(company_name)


            of += 25

    def main(self):
        print('Start scraping...')
        self.pagination()

if __name__ == '__main__':
    proxies = ['80.65.221.12:8800','80.65.220.172:8800','80.65.223.48:8800','80.65.220.133:8800','80.65.221.130:8800',
        '80.65.222.66:8800','80.65.222.138:8800','80.65.223.125:8800','80.65.223.98:8800','80.65.223.188:8800'
    ]

    useragent = 'Jobsearch1.5'

    SSS = SSS(proxies=proxies, useragent=useragent)
    SSS.main()