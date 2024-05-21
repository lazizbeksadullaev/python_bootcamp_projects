"""import requests

# Where USD is the base currency you want to use
url = 'https://v6.exchangerate-api.com/v6/YOUR-API-KEY/latest/USD'

# Making our request
response = requests.get(url)
data = response.json()

# Your JSON object
print(data)
"""

"""
AED UAE Dirham
AFN Afghan Afghani
AED Albanian Lek
AFN Afghan Afghani
ALL Albanian Lek
AMD Armenian Dram
ANG Netherlands Antillian Guilder
AMD Angolan Kwanza
ANG Netherlands Antillian Guilder
AOA Angolan Kwanza
ARS Argentine Peso
AUD Australian Dollar
ARS Aruban Florin
AUD Australian Dollar
AWG Aruban Florin
AZN Azerbaijani Manat
BAM Bosnia and Herzegovina Convertible Mark
AZN Barbados Dollar
BAM Bosnia and Herzegovina Convertible Mark
BBD Barbados Dollar
BDT Bangladeshi Taka
BGN Bulgarian Lev
BDT Bahraini Dinar
BGN Bulgarian Lev
BHD Bahraini Dinar
BIF Burundian Franc
BMD Bermudian Dollar
BIF Brunei Dollar
BMD Bermudian Dollar
BND Brunei Dollar
BOB Bolivian Boliviano
BRL Brazilian Real
BOB Bahamian Dollar
BRL Brazilian Real
BSD Bahamian Dollar
BTN Bhutanese Ngultrum
BWP Botswana Pula
BTN Belarusian Ruble
BWP Botswana Pula
BYN Belarusian Ruble
BZD Belize Dollar
CAD Canadian Dollar
BZD Congolese Franc
CAD Canadian Dollar
CDF Congolese Franc
CHF Swiss Franc
CLP Chilean Peso
CHF Chinese Renminbi
CLP Chilean Peso
CNY Chinese Renminbi
COP Colombian Peso
CRC Costa Rican Colon
COP Cuban Peso
CRC Costa Rican Colon
CUP Cuban Peso
CVE Cape Verdean Escudo
CZK Czech Koruna
CVE Djiboutian Franc
CZK Czech Koruna
DJF Djiboutian Franc
DKK Danish Krone
DOP Dominican Peso
DKK Algerian Dinar
DOP Dominican Peso
DZD Algerian Dinar
EGP Egyptian Pound
ERN Eritrean Nakfa
EGP Ethiopian Birr
ERN Eritrean Nakfa
ETB Ethiopian Birr
EUR Euro
FJD Fiji Dollar
EUR Falkland Islands Pound
FJD Fiji Dollar
FKP Falkland Islands Pound
FOK Faroese Króna
GBP Pound Sterling
FOK Georgian Lari
GBP Pound Sterling
GEL Georgian Lari
GGP Guernsey Pound
GHS Ghanaian Cedi
GGP Gibraltar Pound
GHS Ghanaian Cedi
GIP Gibraltar Pound
GMD Gambian Dalasi
GNF Guinean Franc
GMD Guatemalan Quetzal
GNF Guinean Franc
GTQ Guatemalan Quetzal
GYD Guyanese Dollar
HKD Hong Kong Dollar
GYD Honduran Lempira
HKD Hong Kong Dollar
HNL Honduran Lempira
HRK Croatian Kuna
HTG Haitian Gourde
HRK Hungarian Forint
HTG Haitian Gourde
HUF Hungarian Forint
IDR Indonesian Rupiah
ILS Israeli New Shekel
IDR Manx Pound
ILS Israeli New Shekel
IMP Manx Pound
INR Indian Rupee
IQD Iraqi Dinar
INR Iranian Rial
IQD Iraqi Dinar
IRR Iranian Rial
ISK Icelandic Króna
JEP Jersey Pound
ISK Jamaican Dollar
JEP Jersey Pound
JMD Jamaican Dollar
JOD Jordanian Dinar
JPY Japanese Yen
JOD Kenyan Shilling
JPY Japanese Yen
KES Kenyan Shilling
KGS Kyrgyzstani Som
KHR Cambodian Riel
KGS Kiribati Dollar
KHR Cambodian Riel
KID Kiribati Dollar
KMF Comorian Franc
KRW South Korean Won
KMF Kuwaiti Dinar
KRW South Korean Won
KWD Kuwaiti Dinar
KYD Cayman Islands Dollar
KZT Kazakhstani Tenge
KYD Lao Kip
KZT Kazakhstani Tenge
LAK Lao Kip
LBP Lebanese Pound
LKR Sri Lanka Rupee
LBP Liberian Dollar
LKR Sri Lanka Rupee
LRD Liberian Dollar
LSL Lesotho Loti
LYD Libyan Dinar
LSL Moroccan Dirham
LYD Libyan Dinar
MAD Moroccan Dirham
MDL Moldovan Leu
MGA Malagasy Ariary
MDL Macedonian Denar
MGA Malagasy Ariary
MKD Macedonian Denar
MMK Burmese Kyat
MNT Mongolian Tögrög
MMK Macanese Pataca
MNT Mongolian Tögrög
MOP Macanese Pataca
MRU Mauritanian Ouguiya
MUR Mauritian Rupee
MRU Maldivian Rufiyaa
MUR Mauritian Rupee
MVR Maldivian Rufiyaa
MWK Malawian Kwacha
MXN Mexican Peso
MWK Malaysian Ringgit
MXN Mexican Peso
MYR Malaysian Ringgit
MZN Mozambican Metical
NAD Namibian Dollar
MZN Nigerian Naira
NAD Namibian Dollar
NGN Nigerian Naira
NIO Nicaraguan Córdoba
NOK Norwegian Krone
NIO Nepalese Rupee
NOK Norwegian Krone
NPR Nepalese Rupee
NZD New Zealand Dollar
OMR Omani Rial
NZD Panamanian Balboa
OMR Omani Rial
PAB Panamanian Balboa
PEN Peruvian Sol
PGK Papua New Guinean Kina
PEN Philippine Peso
PGK Papua New Guinean Kina
PHP Philippine Peso
PKR Pakistani Rupee
PLN Polish Złoty
PKR Paraguayan Guaraní
PLN Polish Złoty
PYG Paraguayan Guaraní
QAR Qatari Riyal
RON Romanian Leu
QAR Serbian Dinar
RON Romanian Leu
RSD Serbian Dinar
RUB Russian Ruble
RWF Rwandan Franc
RUB Saudi Riyal
RWF Rwandan Franc
SAR Saudi Riyal
SBD Solomon Islands Dollar
SCR Seychellois Rupee
SBD Sudanese Pound
SCR Seychellois Rupee
SDG Sudanese Pound
SEK Swedish Krona
SGD Singapore Dollar
SEK Saint Helena Pound
SGD Singapore Dollar
SHP Saint Helena Pound
SLE Sierra Leonean Leone
SLL Sierra Leonean Leone
SLE Somali Shilling
SLL Sierra Leonean Leone
SOS Somali Shilling
SRD Surinamese Dollar
SSP South Sudanese Pound
SRD São Tomé and Príncipe Dobra
SSP South Sudanese Pound
STN São Tomé and Príncipe Dobra
SYP Syrian Pound
SZL Eswatini Lilangeni
SYP Thai Baht
SZL Eswatini Lilangeni
THB Thai Baht
TJS Tajikistani Somoni
TMT Turkmenistan Manat
TJS Tunisian Dinar
TMT Turkmenistan Manat
TND Tunisian Dinar
TOP Tongan Paʻanga
TRY Turkish Lira
TOP Trinidad and Tobago Dollar
TRY Turkish Lira
TTD Trinidad and Tobago Dollar
TVD Tuvaluan Dollar
TWD New Taiwan Dollar
TVD Tanzanian Shilling
TWD New Taiwan Dollar
TZS Tanzanian Shilling
UAH Ukrainian Hryvnia
UGX Ugandan Shilling
UAH United States Dollar
UGX Ugandan Shilling
USD United States Dollar
UYU Uruguayan Peso
UZS Uzbekistani So'm
UYU Venezuelan Bolívar Soberano
UZS Uzbekistani So'm
VES Venezuelan Bolívar Soberano
VND Vietnamese Đồng
VUV Vanuatu Vatu
VND Samoan Tālā
VUV Vanuatu Vatu
WST Samoan Tālā
XAF Central African CFA Franc
XCD East Caribbean Dollar
XAF Special Drawing Rights
XCD East Caribbean Dollar
XDR Special Drawing Rights
XOF West African CFA franc
XPF CFP Franc
XOF Yemeni Rial
XPF CFP Franc
YER Yemeni Rial
ZAR South African Rand
ZMW Zambian Kwacha
ZAR Zimbabwean Dollar
ZMW Zambian Kwacha
ZWL Zimbabwean Dollar
54
"""