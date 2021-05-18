import csv
import re
import os
import datetime
import json

json_settings_file = open('./settings.json')
json_settings = json.load(json_settings_file)

SETTINGS = {
    'filename': '',
    'date': json_settings['date'],
    'source': 'CROWDOX',
    'addons': True,
}

json_settings_file.close()

export_dir = './export/' + SETTINGS['date'] + '/'
if not os.path.exists(export_dir):
    os.mkdir(export_dir)

STATE_ABBREV = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands': 'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Palau': 'PW',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
    'Alberta': 'AB',
    'British Columbia': 'BC',
    'Manitoba': 'MB',
    'New Brunswick': 'NB',
    'Newfoundland and Labrador': 'NL',
    'Nova Scotia': 'NS',
    'Ontario': 'ON',
    'Prince Edward Island': 'PE',
    'Quebec': 'QC',
    'Québec': 'QC',
    'Saskatchewan': 'SK',
    'Northern Territories': 'NT',
    'Nunavut': 'NU',
    'Yukon': 'YT',
    'ONTARIO': 'ON',
    'Ca.': 'CA',
    'MISSOURI': 'MO',
    'OR (Oregon)': 'OR',
    'Virginia [VA]': 'VA',
    'FLORIDA': 'FL',
    'CALIFORNIA': 'CA',
    'N Y.': 'NY',
    'texas': 'TX',
    'CO.': 'CO',
    'ILLINOIS': 'IL',
}

SKU_PRICING = {
    'MK-2311G': [99, 10],
    'MK-2311G-LID': [99, 10],
    'MK-2312G-LID': [99, 10],
    'MK-2312T-LID': [99, 10],
    'MK-2311T': [99, 10],
    'MK-2311T-LID': [99, 10],
    'MK-2312G': [99, 10],
    'MK-2312T': [99, 10],
    'MK-2313G': [99, 10],
    'MK-2313G-LID': [99, 10],
    'MK-2313T': [99, 10],
    'MK-2314G': [99, 10],
    'MK-2314G-LID': [99, 10],
    'MK-2314T': [99, 10],
    'MK-2314T-LID': [99, 10],
    'MK-2315G': [99, 10],
    'MK-2315G-LID': [99, 10],
    'MK-2315T': [99, 10],
    'MK-2315T-LID': [99, 10],
    'MK-2321G': [99, 10],
    'MK-2322G': [99, 10],
    'MK-2322T': [99, 10],
    'MK-2323G': [99, 10],
    'MK-2323T': [99, 10],
    'MK-2324G-LID': [99, 10],
    'MK-2324T': [99, 10],
    'MK-2313T-LID': [99, 10],
    'MK-2321G-LID': [99, 10],
    'MK-2321T': [99, 10],
    'MK-2321T-LID': [99, 10],
    'MK-2322G-LID': [99, 10],
    'MK-2322T-LID': [99, 10],
    'MK-2323G-LID': [99, 10],
    'MK-2323T-LID': [99, 10],
    'MK-2324G': [99, 10],
    'MK-2324T-LID': [99, 10],
    'MK-2325G': [99, 10],
    'MK-2325G-LID': [99, 10],
    'MK-2325T': [99, 10],
    'MK-2325T-LID': [99, 10],
}

INTL_SHIPPING = {
    'CA': 20,
    'AU': 55,
    'NZ': 55,
    'IN': 75,
    'IL': 75,
    'HK': 25,
    'SG': 45,
    'TW': 45,
    'JP': 25,
}


def log_error(error, error_file):
    print(error)
    error_file.write(error + '\n')


def trim_length(string, length):
    return string[:length]

filename_suffix = ''
if len(SETTINGS['filename']) > 0:
    filename_suffix = '-' + SETTINGS['filename']

import_filename = './import/' + SETTINGS['date'] + '.csv'
export_filename = export_dir + SETTINGS['date'] + filename_suffix + '.csv'
log_filename = export_dir + SETTINGS['date'] + filename_suffix + '-log.txt'

with open(import_filename) as import_file:
    csv_reader = csv.reader(import_file)
    next(csv_reader)
    with open(export_filename, 'w+') as export_file:
        with open(log_filename, 'w+') as error_file:
            error_file.seek(0)
            error_file.truncate()
            csv_writer = csv.writer(export_file, delimiter=',', quoting=csv.QUOTE_ALL)
            index = 0

            import_headers = ["Order Export Number", "Order Number", "Order Status", "Order Source", "Order Source Number", "Order Source Sequence", "Order Created Date", "Order Invited Date", "Order Paid Date", "Order Completed Date", "Order Canceled Date", "Order Refused Date", "Order Sales Tax", "Order Vat Tax", "Order Customs Tax", "Order Total", "Order Amount Paid", "Order Tax Paid", "Order Shipping Paid", "Order Balance", "Order Internal Notes", "Original Configuration Name", "Configuration Name", "Manage Url", "Survey Url", "Email", "Ship To Company Name", "Ship To Full Name", "Ship To First Name", "Ship To Middle Name", "Ship To Last Name", "Ship To Phone", "Ship To Address 1", "Ship To Address 2", "Ship To Address 3", "Ship To City", "Ship To State", "Ship To Postal Code", "Ship To Country", "Ship To Country Code", "Ship To Location", "Product Bundle", "Product Line", "Product Name", "Product Sku", "Product Quantity", "Product Weight", "Product Length", "Product Width", "Product Height"]

            headers = ["Order Number", "Order Date", "Payment Date", "Buyer Email", "Ship To Name", "Ship To Address 1", "Ship To Address 2", "Ship To Address 3", "Ship To City", "Ship To State", "Ship To Zip Code", "Ship To Country", "Phone Number", "Item SKU", "Order Item Quantity", "Order Item Unit Price", "Customer Ship Amount", "Amount Paid"]
            csv_writer.writerow(headers)

            for row in csv_reader:
                index += 1
                order_number = row[1]

                price = "0"

                if SETTINGS['source'] == 'CROWDOX':
                    order_number = re.sub('CROWDOX-', '', order_number)
                    if SETTINGS['addons'] is True:
                        order_number = order_number + '-1'
                    sku = row[44]
                    quantity = row[45]
                elif SETTINGS['source'] == 'BACKERKIT':
                    sku = row[14]
                    quantity = row[15]

                # Import fields
                if SETTINGS['source'] == 'CROWDOX':
                    raw_date = row[8]

                    if not raw_date:
                        converted_date = datetime.datetime.now()
                    else:
                        converted_date = datetime.datetime.strptime(raw_date, '%m/%d/%Y')
                    transaction_date = converted_date.strftime('%Y-%m-%d %H:%M')

                    email = row[25]
                    # first_name = row[28].replace(',', '').replace('\"', '')
                    # last_name = row[30].replace(',', '').replace('\"', '')
                    # name_length = len(first_name) + len(last_name)
                    # if name_length > 22:
                    #     first_name = trim_length(first_name, name_length - 22)
                    # full_name = first_name + ' ' + last_name
                    full_name = row[27]
                    phone = row[31]
                    address_1 = row[32].replace(',', '')
                    address_2 = row[33].replace(',', '')
                    address_3 = row[34].replace(',', '')
                    city = row[35].replace(',', '')
                    state = row[36].replace(',', '')
                    postal_code = str(row[37]).replace(',', '')
                    country = row[39].replace(',', '')
                elif SETTINGS['source'] == 'BACKERKIT':
                    transaction_date = row[11]
                    email = row[10]
                    name = row[1].replace(',', '').replace('\"', '').rstrip()
                    first_name = ''
                    last_name = ''
                    name_length = len(name)
                    # Split name into first name, last name
                    if name_length > 0:
                        name_list = name.split(' ')
                        last_name = name_list.pop()
                        first_name = ' '.join(name_list)
                        if name_length > 22:
                            first_name = trim_length(first_name, name_length - 22)
                    # full_name = first_name + ' ' + last_name
                    phone = row[9]
                    address_1 = row[2].replace(',', '')
                    address_2 = row[3].replace(',', '')
                    address_3 = ''
                    city = row[4].replace(',', '')
                    state = row[5].replace(',', '')
                    postal_code = str(row[6]).replace(',', '')
                    country = row[7].replace(',', '')

                product_id = "KSSIX"

                if len(state) > 2:
                    if state in STATE_ABBREV:
                        state = STATE_ABBREV[state]
                    elif state.replace('.', '').replace(' ', '') in STATE_ABBREV:
                        state = STATE_ABBREV[state.replace('.', '').replace(' ', '')]
                    else:
                        state = state.replace('.', '').replace(' ', '')

                if len(state) > 2:
                    log_error('Error: State, Order ' + str(order_number) + ', Row ' + str(index) + ': ' + state, error_file)

                if len(postal_code) > 11:
                    log_error('Error: Postal Code, Order ' + str(order_number) + ', Row ' + str(index) + ': ' + postal_code, error_file)
                    postal_code = trim_length(postal_code, 11)
                elif re.search('[^0-9A-Z\-\ ]', postal_code):
                    log_error('Error: Postal Code, Order ' + str(order_number) + ', Row ' + str(index) + ': ' + postal_code, error_file)

                # Shipping calculation
                order_item_unit_price = SKU_PRICING[sku][0]
                customer_ship_amount = SKU_PRICING[sku][1]

                if country != 'US':
                    if country in INTL_SHIPPING:
                        customer_ship_amount = INTL_SHIPPING[country]
                    else:
                        log_error('Error: Country code not included in international shipping')

                amount_paid = order_item_unit_price + customer_ship_amount

                export_row_2 = [
                    order_number,
                    transaction_date,
                    transaction_date,
                    email,
                    full_name,
                    address_1,
                    address_2,
                    address_3,
                    city,
                    state,
                    postal_code,
                    country,
                    phone,
                    sku,
                    quantity,
                    order_item_unit_price,
                    customer_ship_amount,
                    amount_paid,
                ]

                headers = ["Order Number", "Order Date", "Payment Date", "Buyer Email", "Ship To Name", "Ship To Address 1", "Ship To Address 2", "Ship To Address 3", "Ship To City", "Ship To State", "Ship To Zip Code", "Ship To Country", "Item SKU", "Order Item Quantity", "Order Item Unit Price", "Customer Ship Amount", "Amount Paid"]

                csv_writer.writerow(export_row_2)
