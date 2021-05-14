import csv
import re
import os

SETTINGS = {
    'sequence_number': '53',
    'date': '20210223',
    'source': 'CROWDOX',
    'export': 'SKUBANA',
}

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


def log_error(error, error_file):
    print(error)
    error_file.write(error + '\n')


def trim_length(string, length):
    return string[:length]


import_filename = './import/' + SETTINGS['date'] + '.csv'
order_numbers = list()


with open(import_filename) as import_file:
    csv_reader = csv.reader(import_file)
    next(csv_reader)
    with open(export_dir + 'MKSd' + SETTINGS['date'] + '-000' + SETTINGS['sequence_number'] + '-raw.csv', 'w+') as export_file:
        csv_writer = csv.writer(export_file, delimiter='\t', quoting=csv.QUOTE_NONE)
        with open(export_dir + 'MKSh' + SETTINGS['date'] + '-000' + SETTINGS['sequence_number'] + '.csv', 'w+') as export_file_2:
            with open(export_dir + 'MKSe' + SETTINGS['date'] + '-000' + SETTINGS['sequence_number'] + '-errors.txt', 'w+') as error_file:
                error_file.seek(0)
                error_file.truncate()
                csv_writer_2 = csv.writer(export_file_2, delimiter='\t', quoting=csv.QUOTE_NONE)
                index = 0
                export_2_index = 0

                if SETTINGS['export'] == 'SKUBANA':
                    import_headers = ["Order Export Number", "Order Number", "Order Status", "Order Source", "Order Source Number", "Order Source Sequence", "Order Created Date", "Order Invited Date", "Order Paid Date", "Order Completed Date", "Order Canceled Date", "Order Refused Date", "Order Sales Tax", "Order Vat Tax", "Order Customs Tax", "Order Total", "Order Amount Paid", "Order Tax Paid", "Order Shipping Paid", "Order Balance", "Order Internal Notes", "Original Configuration Name", "Configuration Name", "Manage Url", "Survey Url", "Email", "Ship To Company Name", "Ship To Full Name", "Ship To First Name", "Ship To Middle Name", "Ship To Last Name", "Ship To Phone", "Ship To Address 1", "Ship To Address 2", "Ship To Address 3", "Ship To City", "Ship To State", "Ship To Postal Code", "Ship To Country", "Ship To Country Code", "Ship To Location", "Product Bundle", "Product Line", "Product Name", "Product Sku", "Product Quantity", "Product Weight", "Product Length", "Product Width", "Product Height"]

                    headers = ["Order Number", "Order Date", "Payment Date", "Buyer Email", "Ship To Name", "Ship To Address 1", "Ship To Address 2", "Ship To Address 3", "Ship To City", "Ship To State", "Ship To Zip Code", "Ship To Country", "Item SKU", "Order Item Quantity", "Order Item Unit Price", "Customer Ship Amount", "Amount Paid"]
                    csv_writer_2.writerow(headers)

                for row in csv_reader:
                    index += 1
                    order_number = row[0]
                    order_numbers.append(order_number)
                    line_item_number = order_numbers.count(order_number)
                    line_item_number_str = str(line_item_number)

                    if SETTINGS['export'] == 'FOSDICK':
                        price = "0"
                    elif SETTINGS['export'] == 'SKUBANA':
                        price = "0"

                    if SETTINGS['source'] == 'CROWDOX':
                        order_number = re.sub('CROWDOX-', '', order_number)
                        sku = row[44]
                        quantity = row[45]
                    elif SETTINGS['source'] == 'BACKERKIT':
                        sku = row[14]
                        quantity = row[15]

                    if SETTINGS['export'] == 'FOSDICK':
                        export_row_1 = [order_number, line_item_number_str, sku, quantity, price]
                        csv_writer.writerow(export_row_1)

                    # print('Order: ' + order_number + ' Line Item Number: ' + str(line_item_number) + ' SKU: ' + sku + ' Quantity: ' + quantity + ' Price: ' + price)

                    if SETTINGS['export'] == 'FOSDICK':
                        if line_item_number > 1:
                            continue

                    export_2_index += 1

                    # Import fields
                    if SETTINGS['source'] == 'CROWDOX':
                        transaction_date = row[6]
                        transaction_date = re.sub('/', '', transaction_date)
                        email = row[25]
                        first_name = row[28].replace(',', '').replace('\"', '')
                        last_name = row[30].replace(',', '').replace('\"', '')
                        name_length = len(first_name) + len(last_name)
                        if name_length > 22:
                            first_name = trim_length(first_name, name_length - 22)
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
                        phone = row[9]
                        address_1 = row[2].replace(',', '')
                        address_2 = row[3].replace(',', '')
                        address_3 = ''
                        city = row[4].replace(',', '')
                        state = row[5].replace(',', '')
                        postal_code = str(row[6]).replace(',', '')
                        country = row[7].replace(',', '')

                    # Check lengths of all fields for validity
                    if len(email) > 40:
                        email = ''

                    phone = re.sub('[^0-9]', '', phone)
                    if len(phone) > 10:
                        phone = ''

                    address_1 = trim_length(address_1, 30)
                    address_2 = trim_length(address_2, 30)
                    address_3 = trim_length(address_3, 30)
                    product_id = "KSSIX"
                    intl_country = country

                    if SETTINGS['export'] == 'FOSDICK':
                        if country not in {'US', 'CA'}:
                            if len(city) > 30:
                                new_city = trim_length(city, 30)
                                log_error('Error: Intl. City, Order ' + str(order_number) + ', Row ' + str(index) + ': ' + city + ' → ' + new_city, error_file)
                                city = new_city
                            if len(state) > 30:
                                new_state = trim_length(state, 30)
                                log_error('Error: Intl. Province, Order ' + str(order_number) + ', Row ' + str(index) + ': ' + state + ' → ' + new_state, error_file)
                                state = new_state
                            if len(postal_code) > 30:
                                new_postal_code = trim_length(postal_code, 30)
                                log_error('Error: Intl. Postal Code, Order ' + str(order_number) + ', Row ' + str(index) + ': ' + postal_code + ' → ' + new_postal_code, error_file)
                                postal_code = new_postal_code
                            if len(country) > 2:
                                new_country = ''
                                log_error('Error: Intl. Country, Order ' + str(order_number) + ', Row ' + str(index) + ': ' + country + ' → ' + new_country, error_file)
                                country = new_country
                            intl_country = city + '|' + state + '|' + postal_code + '|' + country
                            city = ''
                            state = 'XX'
                            postal_code = 'XXXXX'

                        else:
                            if len(city) > 13:
                                new_city = trim_length(city, 13)
                                # log_error('City Error (trimmed to 13 characters), Row ' + str(index) + ': ' + city + ' → ' + new_city, error_file)
                                city = trim_length(city, 13)
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

                    if SETTINGS['export'] == 'FOSDICK':
                        export_row_2 = [
                            order_number,
                            first_name,
                            last_name,
                            address_1,
                            address_2,
                            address_3,
                            city,
                            state,
                            postal_code,
                            country,
                            phone,
                            "Q",
                            "",
                            "",
                            "",
                            "",
                            "|WEB||",
                            product_id,
                            "",
                            "120000",
                            transaction_date,
                            "",
                            first_name,
                            last_name,
                            address_1,
                            address_2,
                            address_3,
                            city,
                            state,
                            postal_code,
                            intl_country,
                            "1",
                            "",
                            "0.00",
                            "0.00",
                            "0.00",
                            "-0.00",
                            "0.00",
                            email
                        ]
                    elif SETTINGS['export'] == 'SKUBANA':
                        full_name = first_name + ' ' + last_name
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
                            sku,
                            quantity,
                            # order item unit price
                            # customer ship amount
                            # amount paid
                        ]

                    headers = ["Order Number", "Order Date", "Payment Date", "Buyer Email", "Ship To Name", "Ship To Address 1", "Ship To Address 2", "Ship To Address 3", "Ship To City", "Ship To State", "Ship To Zip Code", "Ship To Country", "Item SKU", "Order Item Quantity", "Order Item Unit Price", "Customer Ship Amount", "Amount Paid"]

                    csv_writer_2.writerow(export_row_2)

                if SETTINGS['export'] == 'FOSDICK':
                    # TRAILER RECORD  MKSh20180202    20180202    121212  939 13
                    # trailer record, filename, date, time, number of records, sequence number
                    total_records = index + 1
                    total_records_export_2 = export_2_index + 1
                    trailer_row_d = ['TRAILER RECORD', 'MKSd' + SETTINGS['date'], SETTINGS['date'], '120000', total_records, SETTINGS['sequence_number']]
                    trailer_row_h = ['TRAILER RECORD', 'MKSh' + SETTINGS['date'], SETTINGS['date'], '120000', total_records_export_2, SETTINGS['sequence_number']]
                    csv_writer.writerow(trailer_row_d)
                    csv_writer_2.writerow(trailer_row_h)


# Sheet (1): order number
# Example:
# "500910 1   MK-1072 1   0       "

# Sheet: shipping information
# 500000    Kai Szendi  Alzenauer Platz 6/7/3       Pfaffstaetten 2511  Pfaffstaetten   XX  XXXXX   AT      Q                   | Web | | | KSFN            1312018     Kai Szendi  Alzenauer Platz 6/7/3       Pfaffstaetten 2511  Pfaffstaetten   XX  XXXXX   AT  1       0   0   0   0   0   kickstarter@dev9.org

# Trailer Record example
# TRAILER RECORD  MKSh20180202    20180202    121212  939 13


# Seek each order number in the trailer record
# Determine if it has items that can be combined
    # Put all SKUs in array
# If not, copy order as-is to new trailer record
# If so, rebuild order with appropriate bundle SKUs

"""
with open(export_dir + 'MKSd' + SETTINGS['date'] + '-000' + SETTINGS['sequence_number'] + '-raw.csv') as bundle_import_file:
    bundle_reader = csv.reader(bundle_import_file, delimiter='\t', quoting=csv.QUOTE_NONE)
    with open(export_dir + 'MKSd' + SETTINGS['date'] + '-000' + SETTINGS['sequence_number'] + '.csv', 'w+') as bundle_export_file:
        with open(export_dir + 'MKSe' + SETTINGS['date'] + '-000' + SETTINGS['sequence_number'] + '-errors.txt', 'a+') as error_file:
            csv_writer_bundle = csv.writer(bundle_export_file, delimiter='\t', quoting=csv.QUOTE_NONE)

            row_count = sum(1 for _ in bundle_import_file)
            bundle_import_file.seek(0)

            bundle_index = 0
            bundle_order = []
            bundle_order_skus = []

            for row in bundle_reader:
                bundle_order_number = row[0]
                bundle_line_item_number = row[1]
                bundle_sku = row[2]
                bundle_quantity = row[3]
                bundle_price = "0"
                bundle_export_row = [bundle_order_number, bundle_line_item_number, bundle_sku, bundle_quantity, bundle_price]

                if ((bundle_line_item_number == '1') and (len(bundle_order) > 0)) or (bundle_reader.line_num == row_count):
                    # Check for items to bundle
                    bundle_order_index = 0
                    if all(el in bundle_order_skus for el in ['MK-2211', 'MK-2212', 'MK-2213']):
                        # Exclude above SKUs and add MK-2217
                        log_error('Order Notice: ' + bundle_order[0][0] + ' combined to MK-2217 (Order contains MK-2211, MK-2212, MK-2213)', error_file)
                        bundle_export_row_new = [bundle_order[0][0], '1', 'MK-2217', '1', '0']
                        bundle_index += 1
                        csv_writer_bundle.writerow(bundle_export_row_new)
                        bundle_order_index += 1
                        for bundle_order_line_item in bundle_order:
                            if bundle_order_line_item[2] in ['MK-2211', 'MK-2212', 'MK-2213']:
                                continue
                            else:
                                bundle_order_index += 1
                                bundle_export_row_new = [bundle_order_line_item[0], bundle_order_index, bundle_order_line_item[2], bundle_order_line_item[3], bundle_order_line_item[4]]
                                bundle_index += 1
                                csv_writer_bundle.writerow(bundle_export_row_new)

                    elif all(el in bundle_order_skus for el in ['MK-2211', 'MK-2215']):
                        # Exclude above SKUs and add MK-2217
                        log_error('Order Notice: ' + bundle_order[0][0] + ' combined to MK-2217 (Order contains MK-2215, MK-2211)', error_file)
                        bundle_export_row_new = [bundle_order[0][0], '1', 'MK-2217', '1', '0']
                        bundle_index += 1
                        csv_writer_bundle.writerow(bundle_export_row_new)
                        bundle_order_index += 1
                        for bundle_order_line_item in bundle_order:
                            if bundle_order_line_item[2] in ['MK-2211', 'MK-2215']:
                                continue
                            else:
                                bundle_order_index += 1
                                bundle_export_row_new = [bundle_order_line_item[0], bundle_order_index, bundle_order_line_item[2], bundle_order_line_item[3], bundle_order_line_item[4]]
                                bundle_index += 1
                                csv_writer_bundle.writerow(bundle_export_row_new)

                    elif all(el in bundle_order_skus for el in ['MK-2212', 'MK-2213']):
                        # Exclude above SKUs and add MK-2215
                        log_error('Order Notice: ' + bundle_order[0][0] + ' combined to MK-2215 (Order contains MK-2212, MK-2213)', error_file)
                        bundle_export_row_new = [bundle_order[0][0], '1', 'MK-2215', '1', '0']
                        bundle_index += 1
                        csv_writer_bundle.writerow(bundle_export_row_new)
                        bundle_order_index += 1
                        for bundle_order_line_item in bundle_order:
                            if bundle_order_line_item[2] in ['MK-2212', 'MK-2213']:
                                continue
                            else:
                                bundle_order_index += 1
                                bundle_export_row_new = [bundle_order_line_item[0], bundle_order_index, bundle_order_line_item[2], bundle_order_line_item[3], bundle_order_line_item[4]]
                                bundle_index += 1
                                csv_writer_bundle.writerow(bundle_export_row_new)
                    else:
                        for bundle_order_line_item in bundle_order:
                            bundle_order_index += 1
                            bundle_export_row_new = [bundle_order[0][0], bundle_order_index, bundle_order_line_item[2], bundle_order_line_item[3], bundle_order_line_item[4]]
                            bundle_index += 1
                            csv_writer_bundle.writerow(bundle_export_row_new)

                    # Reset order checking
                    bundle_order = []
                    bundle_order_skus = []

                bundle_order.append(bundle_export_row)
                bundle_order_skus.append(bundle_sku)

            total_records = bundle_index + 1
            trailer_row_d = ['TRAILER RECORD', 'MKSd' + SETTINGS['date'], SETTINGS['date'], '120000', total_records, SETTINGS['sequence_number']]
            csv_writer_bundle.writerow(trailer_row_d)
"""
# Customer with MK-2215 and added MK-2211 > Should be changed to MK-2217
# Customer with MK-2212 and added MK-2213 > Should be changed to MK-2215
# Customer with MK-2213 and added MK-2212 > Should be changed to MK-2215
# Customer who individually had MK-2211, MK-2212 and MK-2213 > Should be changed to MK-2217 (there shouldn't be very many of these)
