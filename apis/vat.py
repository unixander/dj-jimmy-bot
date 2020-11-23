import requests


__all__ = ['VatApi']


VAT_MESSAGE = """<b>{name}</b> ({code})\n"""

PERIOD_MESSAGE = """\n<i>Effective from: {effective_from}</i>\n"""

RATE_MESSAGE = """<b>{name}</b>: {value} \n"""

class VatApi(object):

    base_url = 'https://jsonvat.com/'

    def format_message(self, periods, **kwargs):
        message = VAT_MESSAGE.format(**kwargs)
        for period in periods:
            message += PERIOD_MESSAGE.format(**period)
            for name, value in period.get('rates', {}).items():
                message += RATE_MESSAGE.format(name=name, value=value)
        return message

    def get_vat_rates(self):
        response = requests.get(self.base_url)
        if response.status_code == 200:
            return {r['code']: r for r in response.json()['rates']}
        return None
    
    def format_list(self, rates):
        message = "Enter command: /vat code\n"
        for code, rate in rates.items():
            message += "<b>{name}</b> : <i>{code}</i>\n".format(**rate)
        return message

    def get_vat_rate_by_code(self, code):
        code = code.upper()
        rates = self.get_vat_rates()
        if rates:
            if code in rates:
                return self.format_message(**rates[code])
            else:
                return self.format_list(rates)
        else:
            return 'Enter country code or try again later'
