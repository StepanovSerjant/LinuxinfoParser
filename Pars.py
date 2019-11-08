import smtplib
import os
import datetime
import requests
import openpyexcel
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from bs4 import BeautifulSoup
from openpyexcel.styles import PatternFill, Alignment


class Parser(object):

    def __init__(self, html):

        self.html = html

    def soup(self):

        soup = BeautifulSoup(self.html, 'lxml')

        return soup

    def titles(self, soup):

        # Название каждого элемента
        titles = soup.find('div', {'class': 'view-content view-rows'}).find_all('a')
        title_list = []
        for i in titles:
            title_list.append(i.text)

        return title_list

    def dates(self, soup):
        # Дата каждого элемента
        dates = soup.find('div', {'class': 'view-content view-rows'}).find_all('p', {'class': 'date'})
        date_list = []
        for date in dates:
            date_list.append(date.text)

        return date_list

    def descriptions(self, soup):
        # Описание каждого элемента
        descriptions = soup.find('div', {'class': 'view-content view-rows'}).find_all('div', {'class': 'field-content'})
        desc_list = []
        for item in descriptions:
            desc_list.append(item.text)

        return desc_list

    def links(self, soup):
        # Ссылка каждого элемента
        links = soup.find('div', {'class': 'view-content view-rows'}).find_all('a')
        link_list = []
        for link in links:
            link_part = link['href']
            link = 'https://younglinux.info' + str(link_part)
            link_list.append(link)

        return link_list


class ExcelWriter(object):

    def __init__(self, titles, dates, descriptions, links):
        self.title = titles
        self.date = dates
        self.descriptions = descriptions
        self.links = links

    def writer(self):

        wb = openpyexcel.Workbook()
        ws = wb.active

        # Название листа
        ws.title = 'Свежая сборка статей'

        # Заголовки
        head = ['№', 'Название', 'Дата', 'Описание', 'Ссылка']
        ws.append(head)

        # Закрашиваем заголовки
        fill = PatternFill(fill_type='solid',
                           start_color='FF0000',
                           end_color='FF0000')

        ws['A1'].fill = fill
        ws['B1'].fill = fill
        ws['C1'].fill = fill
        ws['D1'].fill = fill
        ws['E1'].fill = fill

        # Формирование базы данных из словаря и запись в csv
        count = 1
        for i in range(len(self.title)):
            data = [count,
                    self.title[i],
                    self.date[i],
                    self.descriptions[i],
                    self.links[i]]
            count += 1
            ws.append(data)

        # Выравнивание
        align_left = Alignment(horizontal='left',
                                vertical='bottom',
                                text_rotation=0,
                                wrap_text=False,
                                shrink_to_fit=False,
                                indent=0)

        for row in ws.rows:
            for cell in row:
                ws[cell.coordinate].alignment = align_left

        # Растягивание столбцов
        dims = {}
        for row in ws.rows:
            for cell in row:
                if cell.value:
                    dims[cell.column] = max((dims.get(cell.column, 0), len(str(cell.value))))

        for col, value in dims.items():
            if col == 4:
                ws.column_dimensions[col].width = value / 2
            else:
                ws.column_dimensions[col].width = value

        filepath = "linuxoid.xlsx"
        wb.save(filepath)

        return filepath


def send_mail(filepath):
    # Отправка сообщения
    basename = os.path.basename(filepath)

    # Блок текста сообщения с временем
    date = datetime.datetime.now()
    text = 'Сборка статей с сайта на {}-{}-{}. Московское время: {}.'.format(str(date.day),
                                                                             str(date.month),
                                                                             str(date.year),
                                                                             str(date.strftime("%H:%M")))

    # Compose attachment
    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(filepath, "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % basename)

    login = 'your email'
    password = 'password'
    url = 'smtp.yandex.ru'
    send_to = 'email to send'

    msg = MIMEMultipart()
    msg['Subject'] = 'Сборка статей'
    msg['From'] = login
    body = text
    msg.attach(MIMEText(body, 'plain'))
    msg.attach(part)

    server = smtplib.SMTP(url, 587)
    server.ehlo()
    server.starttls()
    server.login(login, password)
    server.sendmail(login, send_to, msg.as_string())
    server.quit()


def main():
    headers = {'accept': '*/*',
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
    url = 'https://younglinux.info'

    session = requests.Session()
    request = session.get(url, headers=headers)

    site = Parser(request.content)

    if request.status_code == 200:

        titles = site.titles(site.soup())
        dates = site.dates(site.soup())
        description = site.descriptions(site.soup())
        links = site.links(site.soup())

        write = ExcelWriter(titles, dates, description, links)
        send_mail(write.writer())

        print('Ждите сообщения на почту. Отправка займет максимум 1-2 минуты.')
    else:
        print('Ошибка соединения')


if __name__ == '__main__':
    main()