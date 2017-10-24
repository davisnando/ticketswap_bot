""" Ticket swap bot """
import json
import sys
import time
import webbrowser

import requests

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup



SESSION_ID = "e828a14793a34421e7259fa71236bee0"
API_KEY = "NTkxYjVkMmM4ZDE1MmJhM2EyMGRmOWUxOGY3MjAyMWUzYjgzYjE5ZDBkOGM4MzI4YWQwNDBjNzE5NmU4MGVkZA"
EVENT_URL = "https://www.ticketswap.nl/event/walibi-halloween-fright-nights/27-oktober/a659e89d-b69f-4cdd-a922-28a643ae0768/453254"
HOST = "https://www.ticketswap.nl"
URL = HOST + "/api/tickets/14c6ccc531/walibi-halloween-fright-nights"
COOKIES = {"api_access_token": API_KEY, "session": SESSION_ID}
AMOUNT = 3

def explode_ticket(ticket_link):
    """ Gets tokens from ticket page """
    # Get tokens that you need to have to reserve the ticket and getting the get in cart link
    response = requests.get(HOST + ticket_link, cookies=COOKIES)
    parsed_html = BeautifulSoup(response.content.decode("utf-8"), "html.parser")

    token_object = parsed_html.body.find('input', attrs={"name":"token"})
    if token_object is None:
        print("Failed to get token")
        return False
    token_attrs = token_object.attrs

    reserve_token_object = parsed_html.body.find('input', attrs={"name":"reserve[_token]"})
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
        global AMOUNT
        if count > AMOUNT:
            add_data['amount'] = AMOUNT
            AMOUNT = 0
        else:
            add_data['amount'] = count
            AMOUNT = AMOUNT - count
    token = token_attrs['value']
    reserve_token = reserve_token_attrs['value']
    ticket_link_reserve = parsed_html.body.find('form', attrs={"id":"listing-reserve-form"}).attrs
    ticket_reserve_link = ticket_link_reserve['data-endpoint']
    return {"token": token,
            "reserve_token": reserve_token,
            "ticket_link": ticket_reserve_link,
            "more_data": add_data}

def get_ticket():
    """ Get Cheapest ticket """
    # Getting the cheapest ticket
    response = requests.get(EVENT_URL, cookies=COOKIES)
    html = response.content.decode("utf-8")
    parsed_html = BeautifulSoup(html, "html.parser")
    not_exist = parsed_html.body.find('div', attrs={'class': "no-tickets"})
    if not_exist is not None:
        return False
    urlobject = parsed_html.body.findAll('a', attrs={'itemprop': "offerurl"})
    if urlobject is None:
        print("no offers")
        return False
    for item in urlobject:
        attributes = item.attrs
        ticket_link = attributes['href']
        data = explode_ticket(ticket_link)
        if data is not False:
            return data
    return False



def reserve_ticket():
    """ Reserve ticket """
    content = get_ticket()
    if content is False:
        return False
    token = content['token']
    reserve_token = content['reserve_token']
    formdata = {"token": token, "reserve[_token]": reserve_token, **content['more_data']}
    # add ticket in cart
    ticket = requests.post(HOST + content['ticket_link'], data=formdata, cookies=COOKIES)
    content = json.loads(ticket.content.decode("utf-8"))
    print('Successfull added ticket to your account')
    return bool(content['success'])


if __name__ == "__main__":
    if  len(sys.argv) >= 2 and sys.argv[1] is not None:
        EVENT_URL = sys.argv[1]
    if len(sys.argv) >= 3 and sys.argv[2] is not None:
        SESSION_ID = sys.argv[2]
    if len(sys.argv) >= 4 and sys.argv[3] is not None:
        AMOUNT = int(sys.argv[3])
    while reserve_ticket() is False or AMOUNT > 0:
        print("Trying again!")
        time.sleep(.5)
    webbrowser.open(HOST + '/cart', new=2)
