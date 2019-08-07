import requests
from bs4 import BeautifulSoup
import smtplib
import os

headerInput = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}


def check_price(URL, header, target_price):
    page = requests.get(URL, headers=header)

    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find(id="productTitle").get_text().strip()
    price = soup.find(id="priceblock_ourprice").get_text()
    converted_price = float(price[5:])

    print(title)
    print(price)

    if converted_price < target_price:
        send_mail(os.environ['email1234'], os.environ['email1234_pass'], converted_price, target_price)
    else:
        print("The price is too high!")


def send_mail(email, email_password, price, target_price):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(email, email_password)

    subject = 'Price fell down!'
    body = 'Your item is below your target price of ' + str(target_price) + '. It is now ' + str(
        price) + '. Get it here: https://www.amazon.ca/Spikeball-Pro-Kit-Tournament-Upgraded/dp/B01M0XJYVO/ref=sr_1_4?keywords=spikeball&qid=1562612864&s=sports&sr=1-4'

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        'philipmorse1234@gmail.com',
        'philipmorse1234@gmail.com',
        msg
    )

    print("The price is below your target. An e-mail has been sent to remind you to purchase it!")
    server.quit()


URLInput = input('Please paste in URL to Amazon Item:\n')
target_price = float(input('What is your target price?'))

check_price(URLInput, headerInput, target_price)
