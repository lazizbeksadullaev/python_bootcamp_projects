import requests

# Where USD is the base currency you want to use
API_KEY = '09dd14accfa86b6658551ea2'

url1 = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD'
dataList = [
    [
        "AED",
        "UAE Dirham"
    ],
    [
        "AFN",
        "Afghan Afghani"
    ],

    [
        "AMD",
        "Armenian Dram"
    ],
    [
        "ANG",
        "Netherlands Antillian Guilder"
    ],
    [
        "ARS",
        "Argentine Peso"
    ],
    [
        "AUD",
        "Australian Dollar"
    ],
    [
        "AZN",
        "Azerbaijani Manat"
    ],
    [
        "BGN",
        "Bulgarian Lev"
    ],
    [
        "BRL",
        "Brazilian Real"
    ],
    [
        "BYN",
        "Belarusian Ruble"
    ],
    [
        "CAD",
        "Canadian Dollar"
    ],
    [
        "CHF",
        "Swiss Franc"
    ],
    [
        "CNY",
        "Chinese Renminbi"
    ],
    [
        "CZK",
        "Czech Koruna"
    ],
    [
        "DKK",
        "Danish Krone"
    ],
    [
        "EGP",
        "Egyptian Pound"
    ],
    [
        "EUR",
        "Euro"
    ],
    [
        "GBP",
        "Pound Sterling"
    ],
    [
        "HKD",
        "Hong Kong Dollar"
    ],
    [
        "HRK",
        "Croatian Kuna"
    ],
    [
        "HUF",
        "Hungarian Forint"
    ],
    [
        "IDR",
        "Indonesian Rupiah"
    ],
    [
        "ILS",
        "Israeli New Shekel"
    ],
    [
        "INR",
        "Indian Rupee"
    ],
    [
        "IQD",
        "Iraqi Dinar"
    ],
    [
        "IRR",
        "Iranian Rial"
    ],
    [
        "ISK",
        "Icelandic Króna"
    ],
    [
        "JPY",
        "Japanese Yen"
    ],
    [
        "KGS",
        "Kyrgyzstani Som"
    ],
    [
        "KRW",
        "South Korean Won"
    ],
    [
        "KWD",
        "Kuwaiti Dinar"
    ],
    [
        "KZT",
        "Kazakhstani Tenge"
    ],
    [
        "LYD",
        "Libyan Dinar"
    ],
    [
        "MXN",
        "Mexican Peso"
    ],
    [
        "MYR",
        "Malaysian Ringgit"
    ],
    [
        "NOK",
        "Norwegian Krone"
    ],
    [
        "NZD",
        "New Zealand Dollar"
    ],
    [
        "PHP",
        "Philippine Peso"
    ],
    [
        "PKR",
        "Pakistani Rupee"
    ],
    [
        "PLN",
        "Polish Złoty"
    ],
    [
        "QAR",
        "Qatari Riyal"
    ],
    [
        "RON",
        "Romanian Leu"
    ],
    [
        "RSD",
        "Serbian Dinar"
    ],
    [
        "RUB",
        "Russian Ruble"
    ],
    [
        "SAR",
        "Saudi Riyal"
    ],
    [
        "SEK",
        "Swedish Krona"
    ],
    [
        "SGD",
        "Singapore Dollar"
    ],
    [
        "SYP",
        "Syrian Pound"
    ],
    [
        "TJS",
        "Tajikistani Somoni"
    ],
    [
        "TMT",
        "Turkmenistan Manat"
    ],
    [
        "TRY",
        "Turkish Lira"
    ],
    [
        "TWD",
        "New Taiwan Dollar"
    ],
    [
        "UAH",
        "Ukrainian Hryvnia"
    ],
    [
        "USD",
        "United States Dollar"
    ],
    [
        "UZS",
        "Uzbekistani So'm"
    ],
    [
        "VND",
        "Vietnamese Đồng"
    ],
    [
        "XDR",
        "Special Drawing Rights"
    ],
    [
        "ZAR",
        "South African Rand"
    ]
]
count = 0

def get_supported_currencies():

    return dataList


def compare_currencies(value, base_currency, target_currency):
    url2 = f'https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{base_currency}/{target_currency}'
    response = requests.get(url2)
    data = response.json()

    # Your JSON object
    # result = f"{data['time_last_update_utc']} holatiga ko'ra\n 1 {base_currency} = {data['conversion_rate']} {target_currency} ga teng"
    calculated = value*data['conversion_rate']
    result = f"{data['time_last_update_utc']} holatiga ko'ra\n{value} {base_currency} = {calculated} {target_currency} ga teng"
    return result


if __name__ == '__main__':
    base_currency = input('''Dastlab chap ustundagi davlatlar pul birligi
    qisqartmasini kiriting va buni 1 birlik deb
    hisoblaymiz misol uchun 1 USD = ? kabi >>>''').upper()
    target_currency = input(f"""Endi yuqorida belgilagan 1 {base_currency} ni qaysi davlat
    pul qiymatiga taqqoslamoqchiligingizni
    qisqartmasini kiriting >>>""").upper()
    print(f"Biz sizga 1 {base_currency} = X {target_currency} ekanligini hisoblab beramiz:")
    value = float(input('value = '))

    print(get_supported_currencies())
    print(compare_currencies(value, base_currency, target_currency))
