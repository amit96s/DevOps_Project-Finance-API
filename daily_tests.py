import os
import requests
import socket
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from create_data_for_today import pull_todays_data
from dotenv import load_dotenv


ip_address = socket.gethostbyname(socket.gethostname())
main_check_status = False

class Test():
    def send_mail(url,error_message):
        sender_email = "TheFisherman.Service@gmail.com"   # Replace with your actual gmail account
        receiver_email = "amitshemesh96@gmail.com"   # Replace to your actual receiver email
        load_dotenv()
        app_password = os.getenv('API_KEY_GOOGLE_MAIL')

        # Create email message
        subject = "Failed: Amit Finance API"
        body = f"Hello amit,\nPlease note that i was unable to access the API service at the address {url}\n" \
               f"Error message: {error_message}."
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, message.as_string())


    def test_all_tickers():
        try:
            url = f'http://{ip_address}'
            response = requests.get(url)
            if response.status_code != 200:
                Test.send_mail(url, response.json())
            main_check_status = True
        except Exception as err:
            Test.send_mail(url, f'Couldnt find any API serivce at {ip_address}')


    def test_top10():
        if main_check_status == True:
            try:
                url = f'http://{ip_address}/top10'
                response = requests.get(url)
                if response.status_code != 200:
                    Test.send_mail(url, 'Endpoint: /top Failed')
            except Exception as err:
                Test.send_mail(url, f'Couldnt find any API serivce at {ip_address}/top10')


    def test_last10():
        if main_check_status == True:
            try:
                url = f'http://{ip_address}/last10'
                response = requests.get(url)
                if response.status_code != 200:
                    Test.send_mail(url, 'Endpoint: /last10 Failed')
            except Exception as err:
                Test.send_mail(url, f'Couldnt find any API serivce at {ip_address}/last10')

    def test_ticker_prices():
        if main_check_status == True:
            try:
                url = f'http://{ip_address}/tsla'
                response = requests.get(url)
                if response.status_code != 200:
                    Test.send_mail(url, 'Endpoint: /tsla')
            except Exception as err:
                Test.send_mail(url, f'Couldnt find any API serivce at {ip_address}/tsla')



    def test_ticker_info():
        if main_check_status == True:
            try:
                url = f'http://{ip_address}/info/tsla'
                response = requests.get(url)
                if response.status_code != 200:
                    Test.send_mail(url, 'Endpoint: /info/tsla')
            except Exception:
                Test.send_mail(url, f'Couldnt find any API serivce at {ip_address}/info/tsla')


pull_todays_data()
Test.test_all_tickers()
Test.test_top10()
Test.test_last10()
Test.test_ticker_prices()