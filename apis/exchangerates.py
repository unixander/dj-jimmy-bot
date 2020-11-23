import requests 

__all__ = ['ExchangeRatesApi']

CURRENCY_TEMPLATE = """
Base: *{base}*
--------------
usd | 12
--- | ---
"""


class ExchangeRatesApi(object):

    base_url = 'https://exchangeratesapi.io/api'

    def __init__(self):
        self.session = requests.Session()

    def get_currencies(self):
        response = self.session.get('{}/latest'.format(self.base_url), params={'base': 'USD'})
        if response.status_code == 200:
            return response.json()
        return None

    def get_currencies_message(self, currencies=None):
        data = self.get_currencies()

        if data is None:
            return None

        rates = {}
        if currencies:
            for currency in currencies:
                rates[currency.upper()] = data['rates'].get(currency.upper())
        else:
            rates = data['rates']

        return CURRENCY_TEMPLATE
