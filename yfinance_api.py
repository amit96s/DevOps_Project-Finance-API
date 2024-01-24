import os
import openai
from flask import jsonify
from flask_smorest import Blueprint
from flask.views import MethodView
import yfinance as yf
import pandas as pd
from datetime import datetime
from create_data_for_today import pull_todays_data
from dotenv import load_dotenv
from schemas import StockDataSchema, InfoSchema


blp = Blueprint("Nasdaq Stocks",__name__, description='Information about shares in the Nasdaq index')


@blp.route("/")
class AllTickers(MethodView):
    @blp.response(200, StockDataSchema(many=True), description="A list of all the stocks in the nasdaq index with the most recent change for each one")
    def get(self):
        """ All Nasdaq stocks and their last change %"""
        return jsonify(pull_todays_data())



@blp.route("/top10")
class All_top10(MethodView):
    @blp.response(200, StockDataSchema(many=True), description='Top 10 preforming stock in the Nasdaq index')
    def get(self):
        """ Top 10 preforming stock in the Nasdaq index"""
        data_file = pd.read_csv(f'data-{datetime.now().date()}.csv')
        top10 = data_file.sort_values(by=['Change'], ascending=False).head(10)
        top10['place'] = range(1, 11)

        return jsonify(top10.to_dict(orient='records')),200


@blp.route("/last10")
class All_last10(MethodView):
    @blp.response(200, StockDataSchema(many=True), description='Last 10 preforming stock in the Nasdaq index')
    def get(self):
        """ Last 10 preforming stock in the Nasdaq index"""
        try:
            data_file = pd.read_csv(f'data-{datetime.now().date()}.csv')
            top10 = data_file.sort_values(by=['Change'], ascending=True).head(10)
            top10['place'] = range(1, 11)
            return jsonify(top10.to_dict(orient='records')), 200
        except Exception:
            return jsonify({"Message": "Sorry, we have a problem with this address, we are taking care of it"}, 404)



@blp.route("/<string:ticker>")
class All_Tickers(MethodView):
    @blp.response(200,StockDataSchema(many=True), description='Closing prices of a specific ticker over the last 30 days')
    def get(self,ticker):
        """ Closing prices of a specific ticker over the last 30 days"""
        try:
            stock = yf.Ticker(ticker)
            close_prices = stock.history(period='30d')['Close']
            if close_prices.empty:
                return {"Message":f"Sorry, couldnt find any price data on {ticker}"}, 404
            close_prices = close_prices.reset_index()
            close_prices['Close'] = close_prices['Close'].round(2)
            close_prices['Date'] = close_prices['Date'].dt.strftime("%Y-%m-%d")
            return jsonify(close_prices.iloc[::-1].to_dict(orient='records')), 200
        except Exception:
            return jsonify({"Message": "Sorry, we have a problem with this address, we are taking care of it"}, 404)



@blp.route("/info/<string:ticker>")
class All_Tickers(MethodView):
    @blp.response(200, InfoSchema, description="Company information")
    def get(self,ticker):
        """ Brief overview of the company's general information"""
        try:
            chat_gpt_promt = f'what is the ticker of the {ticker} in the stock exchange?' \
                             f' If you think this is a company traded on the stock exchange,' \
                             f' give me a summary of what it does, what is special about it,' \
                             f' and a little about the financial aspect of Aliya in terms of the capital market. ' \
                             f'make it short. If you think this is not' \
                             f' a publicly traded company and you dont know what its ticker is, answer with the exacl message and nothing else:' \
                             f' "Im not sure its a publicly traded company"'

            if f'{ticker}.txt' in os.listdir():
                return jsonify(open(f'{ticker}.txt','r').read())


            else:
                load_dotenv()
                openai.api_key = os.getenv('API_KEY')
                answer = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": chat_gpt_promt}])

                answer = str(answer.choices[0].message.content)
                if "not sure" not in answer:
                    with open(f'{ticker}.txt','w') as file:
                        file.write(answer)

                    return jsonify(answer),200

                return jsonify({"Message":f'{answer}'}),404

        except:
            return jsonify({"Message":"Sorry, service is not available now due to Openai API issue"})