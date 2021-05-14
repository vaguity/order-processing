import csv
# import re
import os
import datetime

SETTINGS = {
    'date': '20210304',
    'filename': '1',
    'source': 'BACKERKIT',
    'export': 'SKUBANA',
}

export_dir = './export/' + SETTINGS['date'] + '/'
if not os.path.exists(export_dir):
    os.mkdir(export_dir)

if len(SETTINGS['filename']) > 0:
    filename_suffix = '-' + SETTINGS['filename']

import_filename = './import/' + SETTINGS['date'] + filename_suffix + '.csv'
export_filename = export_dir + SETTINGS['date'] + filename_suffix + '.csv'
log_filename = export_dir + SETTINGS['date'] + filename_suffix + '-log.txt'


def convert_row_to_skubana(row):

    order_number = row[0]
    raw_date = row[11]
    email = row[10]
    name = row[1]
    address_1 = row[2]
    address_2 = row[3]
    city = row[4]
    state = row[5]
    postal_code = row[6]
    country = row[7]
    sku = row[14]
    quantity = row[15]

    # SKU price, shipping price
    sku_pricing = {
        'MK-2212': [55, 6],
        'MK-2213': [75, 6],
        'MK-2215': [99, 9],
        'MK-6300': [0, 0],
        'MK-6301': [12, 2],
        'MK-2211': [30, 5],
        'MK-2212': [55, 5],
        'MK-2213': [75, 5],
        'MK-2215': [99, 10],
        'MK-2217': [129, 10],
        'MK-1011-2': [55, 2],
        'MK-1012-2': [55, 2],
        'MK-1013-2': [55, 2],
        'MK-1021-2': [25, 2],
        'MK-1022-2': [25, 2],
        'MK-1023-2': [25, 2],
        'MK-1031-2': [50, 2],
        'MK-1032-2': [50, 2],
        'MK-1033-2': [50, 2],
        'MK-1041-2': [55, 2],
        'MK-1042-2': [55, 2],
        'MK-1043-2': [55, 2],
        'MK-1051-2': [40, 2],
        'MK-1052-2': [40, 2],
        'MK-1053-2': [40, 2],
        'MK-1071-2': [110, 5],
        'MK-1072-2': [110, 5],
        'MK-1073-2': [110, 5],
        'MK-1081-2': [170, 5],
        'MK-1082-2': [170, 5],
        'MK-1083-2': [170, 5],
    }

    if not raw_date:
        converted_date = datetime.datetime.now()
    else:
        converted_date = datetime.datetime.strptime(raw_date, '%Y-%m-%d %H:%M:%S %z')
    date = converted_date.strftime('%Y-%m-%d %H:%M')

    export_row = [
        order_number,
        date,
        date,
        email,
        name,
        address_1,
        address_2,
        "",
        city,
        state,
        postal_code,
        country,
        sku,
        quantity,
        sku_pricing[sku][0],
        sku_pricing[sku][1],
        sku_pricing[sku][0] + sku_pricing[sku][1]
    ]

    return export_row


with open(import_filename) as import_file:
    csv_reader = csv.reader(import_file)
    next(csv_reader)
    with open(export_filename, 'w+') as export_file:
        csv_writer = csv.writer(export_file, quoting=csv.QUOTE_ALL)
        with open(log_filename, 'w+') as log_file:
            log_writer = csv.writer(log_file)

            if SETTINGS['export'] == 'FLOSHIP':
                export_headers = ["Backer ID", "Name", "Address Line 1", "Address Line 2", "Address City", "Address State", "Address Postal Code", "Address Country", "Full Address", "Address Phone", "Email", "Pledged At", "Notes", "Sku Name", "Sku Code", "Quantity"]
            elif SETTINGS['export'] == 'SKUBANA':
                export_headers = ["Order Number", "Order Date", "Payment Date", "Buyer Email", "Ship To Name", "Ship To Address 1", "Ship To Address 2", "Ship To Address 3", "Ship To City", "Ship To State", "Ship To Zip Code", "Ship To Country", "Item SKU", "Order Item Quantity", "Order Item Unit Price", "Customer Ship Amount", "Amount Paid"]

            csv_writer.writerow(export_headers)

            # Batch orders by order number, assumes order line items are continguous

            order_items = []
            order_skus = []
            previous_order_id = ''
            for row in csv_reader:
                order_id = row[0]
                order_sku = row[14]
                # Check for end of batch
                if (order_id == previous_order_id) or (previous_order_id == ''):
                    pass
                else:
                    # Process batch
                    if all(el in order_skus for el in ['MK-2211', 'MK-2212', 'MK-2213']):
                        # Exclude above SKUs and add MK-2217
                        for order_item in order_items:
                            if order_item[14] in ['MK-2211', 'MK-2212', 'MK-2213']:
                                # Ignore unneeded order items
                                pass
                            else:
                                # Rewrite order_item to match Skubana format
                                # Write row to export file
                                if SETTINGS['export'] == 'FLOSHIP':
                                    csv_writer.writerow(order_item)
                                elif SETTINGS['export'] == 'SKUBANA':
                                    skubana_order_item = convert_row_to_skubana(order_item)
                                    csv_writer.writerow(skubana_order_item)

                        # Add MK-2217
                        export_row = order_items[0]
                        export_row[14] = 'MK-2217'
                        if SETTINGS['export'] == 'FLOSHIP':
                            csv_writer.writerow(export_row)
                        elif SETTINGS['export'] == 'SKUBANA':
                            skubana_order_item = convert_row_to_skubana(export_row)
                            csv_writer.writerow(skubana_order_item)
                        log_message = 'Order #' + order_items[0][0] + ': MK-2211, MK-2212, and MK-2213 combined to MK-2217'
                        log_writer.writerow([log_message])
                        print(log_message)
                    elif all(el in order_skus for el in ['MK-2211', 'MK-2215']):
                        # Exclude above SKUs and add MK-2217
                        for order_item in order_items:
                            if order_item[14] in ['MK-2211', 'MK-2215']:
                                # Ignore uneeded order items
                                pass
                            else:
                                # Write row to export file
                                if SETTINGS['export'] == 'FLOSHIP':
                                    csv_writer.writerow(order_item)
                                elif SETTINGS['export'] == 'SKUBANA':
                                    skubana_order_item = convert_row_to_skubana(order_item)
                                    csv_writer.writerow(skubana_order_item)
                        # Add MK-2217
                        export_row = order_items[0]
                        export_row[14] = 'MK-2217'
                        if SETTINGS['export'] == 'FLOSHIP':
                            csv_writer.writerow(export_row)
                        elif SETTINGS['export'] == 'SKUBANA':
                            skubana_order_item = convert_row_to_skubana(export_row)
                            csv_writer.writerow(skubana_order_item)
                        log_message = 'Order #' + order_items[0][0] + ': MK-2211 and MK-2215 combined to MK-2217'
                        log_writer.writerow([log_message])
                        print(log_message)
                    elif all(el in order_skus for el in ['MK-2212', 'MK-2213']):
                        # Exclude above SKUs and add MK-2215
                        for order_item in order_items:
                            if order_item[14] in ['MK-2212', 'MK-2213']:
                                # Ignore uneeded order items
                                pass
                            else:
                                # Write row to export file
                                if SETTINGS['export'] == 'FLOSHIP':
                                    csv_writer.writerow(order_item)
                                elif SETTINGS['export'] == 'SKUBANA':
                                    skubana_order_item = convert_row_to_skubana(order_item)
                                    csv_writer.writerow(skubana_order_item)
                        # Add MK-2215
                        export_row = order_items[0]
                        export_row[14] = 'MK-2215'
                        if SETTINGS['export'] == 'FLOSHIP':
                            csv_writer.writerow(export_row)
                        elif SETTINGS['export'] == 'SKUBANA':
                            skubana_order_item = convert_row_to_skubana(export_row)
                            csv_writer.writerow(skubana_order_item)
                        log_message = 'Order #' + order_items[0][0] + ': MK-2212 and MK-2213 combined to MK-2215'
                        log_writer.writerow([log_message])
                        print(log_message)
                    else:
                        for order_item in order_items:
                            # Write row to export file
                            if SETTINGS['export'] == 'FLOSHIP':
                                csv_writer.writerow(order_item)
                            elif SETTINGS['export'] == 'SKUBANA':
                                skubana_order_item = convert_row_to_skubana(order_item)
                                csv_writer.writerow(skubana_order_item)
                        # print('Order #' + order_items[0][0] + ': Unedited')

                    order_items = []
                    order_skus = []

                order_items.append(row)
                order_skus.append(order_sku)
                previous_order_id = order_id

            if (len(order_items) > 0):
                # Process final batch
                if all(el in order_skus for el in ['MK-2211', 'MK-2212', 'MK-2213']):
                    # Exclude above SKUs and add MK-2217
                    for order_item in order_items:
                        if order_item[14] in ['MK-2211', 'MK-2212', 'MK-2213']:
                            # Ignore uneeded order items
                            pass
                        else:
                            # Write row to export file
                            if SETTINGS['export'] == 'FLOSHIP':
                                csv_writer.writerow(order_item)
                            elif SETTINGS['export'] == 'SKUBANA':
                                skubana_order_item = convert_row_to_skubana(order_item)
                                csv_writer.writerow(skubana_order_item)
                    # Add MK-2217
                    export_row = order_items[0]
                    export_row[14] = 'MK-2217'
                    if SETTINGS['export'] == 'FLOSHIP':
                        csv_writer.writerow(export_row)
                    elif SETTINGS['export'] == 'SKUBANA':
                        skubana_order_item = convert_row_to_skubana(export_row)
                        csv_writer.writerow(skubana_order_item)
                    log_message = 'Order #' + order_items[0][0] + ': MK-2211, MK-2212, and MK-2213 combined to MK-2217'
                    log_writer.writerow([log_message])
                    print(log_message)
                elif all(el in order_skus for el in ['MK-2211', 'MK-2215']):
                    # Exclude above SKUs and add MK-2217
                    for order_item in order_items:
                        if order_item[14] in ['MK-2211', 'MK-2215']:
                            # Ignore uneeded order items
                            pass
                        else:
                            # Write row to export file
                            if SETTINGS['export'] == 'FLOSHIP':
                                csv_writer.writerow(order_item)
                            elif SETTINGS['export'] == 'SKUBANA':
                                skubana_order_item = convert_row_to_skubana(order_item)
                                csv_writer.writerow(skubana_order_item)
                    # Add MK-2217
                    export_row = order_items[0]
                    export_row[14] = 'MK-2217'
                    if SETTINGS['export'] == 'FLOSHIP':
                        csv_writer.writerow(export_row)
                    elif SETTINGS['export'] == 'SKUBANA':
                        skubana_order_item = convert_row_to_skubana(export_row)
                        csv_writer.writerow(skubana_order_item)
                    log_message = 'Order #' + order_items[0][0] + ': MK-2211 and MK-2215 combined to MK-2217'
                    log_writer.writerow([log_message])
                    print(log_message)
                elif all(el in order_skus for el in ['MK-2212', 'MK-2213']):
                    # Exclude above SKUs and add MK-2215
                    for order_item in order_items:
                        if order_item[14] in ['MK-2212', 'MK-2213']:
                            # Ignore uneeded order items
                            pass
                        else:
                            # Write row to export file
                            if SETTINGS['export'] == 'FLOSHIP':
                                csv_writer.writerow(order_item)
                            elif SETTINGS['export'] == 'SKUBANA':
                                skubana_order_item = convert_row_to_skubana(order_item)
                                csv_writer.writerow(skubana_order_item)
                    # Add MK-2215
                    export_row = order_items[0]
                    export_row[14] = 'MK-2215'
                    if SETTINGS['export'] == 'FLOSHIP':
                        csv_writer.writerow(export_row)
                    elif SETTINGS['export'] == 'SKUBANA':
                        skubana_order_item = convert_row_to_skubana(export_row)
                        csv_writer.writerow(skubana_order_item)
                    log_message = 'Order #' + order_items[0][0] + ': MK-2212 and MK-2213 combined to MK-2215'
                    log_writer.writerow([log_message])
                    print(log_message)
                else:
                    for order_item in order_items:
                        # Write row to export file
                        if SETTINGS['export'] == 'FLOSHIP':
                            csv_writer.writerow(order_item)
                        elif SETTINGS['export'] == 'SKUBANA':
                            skubana_order_item = convert_row_to_skubana(order_item)
                            csv_writer.writerow(skubana_order_item)
                    # print('Order #' + order_items[0][0] + ': Unedited')

                order_items = []
                order_skus = []
