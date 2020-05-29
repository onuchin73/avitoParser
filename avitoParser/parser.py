import datetime
import urllib.parse
from collections import namedtuple
import bs4
import requests


InnerBlock = namedtuple('Block', 'title,price,currency,date,url')


class Block(InnerBlock):

    def __str__(self):
        return f'{self.title}\t{self.price} {self.currency}\t{self.date}\t{self.url}'


class AvitoParser:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
            'Accept-Language': 'ru',
        }

    def get_page(self, page: int = None):
        params = {
            'radius': 200,
            # 'user': 1,
        }
        if page and page > 1:
            params['p'] = page

        url = 'https://www.avito.ru/kazan/avtomobili/hyundai/accent-ASgBAgICAkTgtg2imzHitg2kmzE?radius=0'
        r = self.session.get(url, params=params)
        return r.text

    @staticmethod
    def parse_date(item: str):
        params = item.strip().split(' ')
        # print(params)
        if len(params) == 2:
            day, time = params
            if day == 'Сегодня':
                date = datetime.date.today()
            elif day == 'Вчера':
                date = datetime.date.today() - datetime.timedelta(days=1)
            else:
                print('Не смогли разобрать день:', item)
                return

            time = datetime.datetime.strptime(time, '%H:%M').time()
            return datetime.datetime.combine(date=date, time=time)

        elif len(params) == 3:
            day, month_hru, time = params
            day = int(day)
            months_map = {
                'января': 1,
                'февраля': 2,
                'марта': 3,
                'апреля': 4,
                'мая': 5,
                'июня': 6,
                'июля': 7,
                'августа': 8,
                'сентября': 9,
                'октября': 10,
                'ноября': 11,
                'декабря': 12,
            }
            month = months_map.get(month_hru)
            if not month:
                print('Не смогли разобрать месяц:', item)
                return

            today = datetime.datetime.today()
            time = datetime.datetime.strptime(time, '%H:%M')
            return datetime.datetime(day=day, month=month, year=today.year, hour=time.hour, minute=time.minute)

        else:
            print('Не смогли разобрать формат:', item)
            return

    def parse_block(self, item):
        # Выбрать блок со ссылкой
        url_block = item.select_one('a.snippet-link')
        href = url_block.get('href')
        if href:
            url = 'https://www.avito.ru' + href
        else:
            url = None

        # Выбрать блок с названием
        title_block = item.select_one('a.snippet-link')
        title = url_block.get('title')
        # Подумать с названием
        #        title = title_block.string.strip()

        # Выбрать блок с названием и валютой
        price_block = item.select_one('span.snippet-price')
        price_block = price_block.get_text('\n')
        price_block = list(filter(None, map(lambda i: i.strip(), price_block.split('\n'))))
        if len(price_block) == 2:
            price, currency = price_block
        elif len(price_block) == 1:
            # Бесплатно
            price, currency = 0, None
        else:
            price, currency = None, None
            print(f'Что-то пошло не так при поиске цены: {price_block}, {url}')

        # Выбрать блок с датой размещения объявления
        date = None
        date_block = item.select_one('div.snippet-date-info')
        absolute_date = date_block.get('data-tooltip')
        if absolute_date:
            date = self.parse_date(item=absolute_date)

        return Block(
            url=url,
            title=title,
            price=price,
            currency=currency,
            date=date,
        )

    def get_pagination_limit(self):
        text = self.get_page()
        soup = bs4.BeautifulSoup(text, 'lxml')
        container = soup.select('a.pagination-page')
        last_button = container[-1]
        href = last_button.get('href')
        if not href:
            return 1

        r = urllib.parse.urlparse(href)
        params = urllib.parse.parse_qs(r.query)
        return int(params['p'][0])

    def get_blocks(self, page: int = None):
        text = self.get_page(page=page)
        soup = bs4.BeautifulSoup(text, 'lxml')
        container = soup.select(
            'div.snippet-horizontal.item.item_table.clearfix.js-catalog-item-enum.item-with-contact.js-item-extended')
        for item in container:
            block = self.parse_block(item=item)
            print(block)

    def parse_all(self):
        limit = self.get_pagination_limit()
        print(f'Всего страниц: {limit}')

        for i in range(1, limit + 1):
            self.get_blocks(page=i)


def main():
    p = AvitoParser()
    p.parse_all()


if __name__ == '__main__':
    main()
