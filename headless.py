""" Ticket swap bot """
import json
import time
import webbrowser
import requests
import getpass


from selenium import webdriver
from pyvirtualdisplay import Display

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

HOST = "https://www.ticketswap.nl"


class TicketSwap:
    def __init__(self):
        self.login()
        self.has_tickets = False

    def login(self):
        username = input('Facebook username: ')
        password = getpass.getpass('Facebook password: ')
        display = Display(visible=0, size=(1366, 768))
        display.start()

        driver = webdriver.Chrome()
        driver.get(HOST)
        login_button = driver.find_element_by_class_name(
                    'main-navigation--desktop').find_elements_by_tag_name('li')[1]
        login_button.click()
        time.sleep(1)

        driver.switch_to_window(driver.window_handles[1])
        userInput = driver.find_element_by_id('email')
        passInput = driver.find_element_by_id('pass')

        userInput.send_keys(username)
        passInput.send_keys(password)

        send_login = driver.find_element_by_id('u_0_0')
        send_login.click()

        time.sleep(1)

        driver.switch_to_window(driver.window_handles[0])

        time.sleep(3)

        self.cookies = self.__handle_cookies(driver.get_cookies())

        driver.quit()
        
        display.stop()

    def __handle_cookies(self, cookieList):
        cookies = {}
        for cookie in cookieList:
            cookies[cookie['name']] = cookie['value']
        return cookies

    def start(self):
        eventurl = input('Type here the event url: ')
        while self.has_tickets is False:
            print('Checking for tickets')
            data = self.get_ticket(eventurl)
            if data is not False:
                self.reserve_ticket(data)
                self.has_tickets = True
                webbrowser.open(HOST + '/cart', new=2)
            time.sleep(1)

    def get_ticket(self, eventurl):
        """ Get Cheapest ticket """
        # Getting the cheapest ticket
        response = requests.get(eventurl, cookies=self.cookies)
        html = response.content.decode("utf-8")
        with open('test.html', 'w') as filename:
            filename.write(html)
        
        parsed_html = BeautifulSoup(html, "html.parser")
        not_exist = parsed_html.body.find('div', attrs={'class': "no-tickets"})
        if not_exist is not None:
            print("no tickets")
            return False
        urlobject = parsed_html.body.findAll('a', attrs={'itemprop': "offerurl"})
        if urlobject is None:
            print("no offers")
            return False
        for item in urlobject:
            attributes = item.attrs
            ticket_link = attributes['href']
            data = self.explode_ticket(ticket_link)
            if data is not False:
                return data
        print('Possible that you have the wrong event url')
        return False

    def explode_ticket(self, ticket_link):
        """ Gets tokens from ticket page """
        # Get tokens that you need to have to reserve the ticket and getting the get in cart link
        response = requests.get(HOST + ticket_link, cookies=self.cookies)
        parsed_html = BeautifulSoup(response.content.decode("utf-8"), "html.parser")
        token_object = parsed_html.body.find('input', attrs={"name": "token"})
        if token_object is None:
            print("Failed to get token")
            return False
        token_attrs = token_object.attrs
        reserve_token_object = parsed_html.body.find('input', attrs={"name": "reserve[_token]"})

        if reserve_token_object is None:
            return False
        reserve_token_attrs = reserve_token_object.attrs
        # check type of ticket
        add_data = {}
        seats = parsed_html.body.find('input', attrs={'name': 'tickets[]'})
        if seats is not None:
            add_data['tickets[]'] = seats.attrs['value']
        else:
            items = parsed_html.body.find('select', attrs={'id': 'listing-show-amount'})
            count = len(items.findChildren())
            add_data['amount'] = count
        token = token_attrs['value']
        reserve_token = reserve_token_attrs['value']
        ticket_link_reserve = parsed_html.body.find('form', attrs={"id": "listing-reserve-form"}).attrs
        ticket_reserve_link = ticket_link_reserve['data-endpoint']
        return {"token": token,
                "reserve_token": reserve_token,
                "ticket_link": ticket_reserve_link,
                "more_data": add_data}

    def reserve_ticket(self, content):
        """ Reserve ticket """
        token = content['token']
        reserve_token = content['reserve_token']
        formdata = {"token": token, "reserve[_token]": reserve_token, **content['more_data']}
        # add ticket in cart
        ticket = requests.post(HOST + content['ticket_link'], data=formdata, cookies=self.cookies)
        content = json.loads(ticket.content.decode("utf-8"))
        print('Successfull added ticket to your account')
        return bool(content['success'])


if __name__ == "__main__":
    t = TicketSwap()
    t.start()

