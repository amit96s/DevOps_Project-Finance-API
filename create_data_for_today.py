from datetime import datetime
import pandas as pd
import yfinance as yf
import requests
from flask import jsonify
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

def pull_todays_data():
        try:
            data_file = f'data-{datetime.now().date()}.csv'
            if data_file in os.listdir():
                return pd.read_csv(data_file).to_dict(orient='records')
            else:
                url = 'https://en.wikipedia.org/wiki/Nasdaq-100#Components'
                response = requests.get(url)
                tables = pd.read_html(response.text)
                nasdaq = tables[4]
                nasdaq_df = pd.DataFrame({"Ticker": nasdaq['Ticker'].tolist(), "Company": nasdaq['Company'].tolist()})
                change_column = pd.DataFrame(columns=['Ticker','Change'])
                for ticker in nasdaq_df.iterrows():
                    stock = yf.Ticker(ticker[1]['Ticker'])
                    close_prices = stock.history(period='2d')['Close']
                    last_price = close_prices[1]
                    two_days_ago_price = close_prices[0]
                    if (
                        isinstance(last_price, float) and
                        isinstance(two_days_ago_price, float)
                    ):

                        change = round((((float(last_price)/float(two_days_ago_price))-1)*100),3)
                        new_row = pd.DataFrame({'Ticker': [ticker[1]['Ticker']], 'Change': [change]})
                        change_column = pd.concat([change_column, new_row], ignore_index=True)

                nasdaq_df_with_change_col = pd.merge(nasdaq_df, change_column, on='Ticker', how='left')
                nasdaq_df_with_change_col.to_csv(f'data-{datetime.now().date()}.csv', index=False)

                return jsonify(nasdaq_df_with_change_col.to_dict(orient='records'))
        except RuntimeError as ignore_error:
            pass
        except Exception as err:
            load_dotenv()
            sender_email = "TheFisherman.Service@gmail.com" # Replace with your actual gmail account
            receiver_email = "amitshemesh96@gmail.com"    # Replace to your actual receiver email
            app_password = os.getenv('API_KEY_GOOGLE_MAIL')

            # Create the email message
            subject = "Failed: Amit Finance API"
            body = f"Hello amit,\nPlease note that pulling data for {datetime.now().date()} failed" \
                   f"\nError message:{err}."
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))

            context = ssl.create_default_context()

            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, app_password)
                server.sendmail(sender_email, receiver_email, message.as_string())

            return jsonify({"Message:":"Sorry for the inconvenience, but due to a server malfunction I am unable to display"
                               " data for the last day."})

pull_todays_data()