import smtplib
import time
import requests as rq
from datetime import date
from bs4 import BeautifulSoup

# Enter the website link you want to scrape
site = 'https://www.eponuda.com/ram-memorija-cene/kingston-ddr4-8gb-2666mhz-hyperx-fury-black-hx426c16fb3-8-ram-memorija-cena-497745'
header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}

# Minimal price that i'm interested in
minimal_price = 4500

def get_price():
    html = rq.get(site, headers=header).text
    soup = BeautifulSoup(html, 'html.parser')
    # Find an <a> tag with href='#cene'
    # Yours will be different 
    price = soup.find('a', {'href': '#cene'}).text

    # I did some string manipulation so that i can get just the price
    return price.split()[2][0:5]

site_price = float(get_price()) * 1000 

while True:
    # Compares the minimal price to the actual price
    # If it's good enough send me the email and notify me
    if minimal_price > site_price:
        # if you're using some other email then change
        # 'smtp.google.com' or something
        server = smtplib.SMTP('smtp.live.com', 587)
        server.ehlo()
        server.starttls()

        # Your email credentials
        server.login('YOUR_EMAIL', 'YOUR_PASSWORD')

        # Subject of the email
        subject = 'EPonuda cena za ram opala!'
        
        # What should be in the body
        body = 'Pala cena za ram: https://www.eponuda.com/ram-memorija-cene/kingston-ddr4-8gb-2666mhz-hyperx-fury-black-hx426c16fb3-8-ram-memorija-cena-497745'
        msg = f'Subject:{subject}\n\n{body}'

        # Send the email, from, to, message
        server.sendmail('FROM', 'TO', msg)

        print('Email sent!')
        server.quit()
    else:
        print(f'{date.today()} the price is still not good enough!')   
    # Sleeps for a day
    time.sleep(86400)
    