import csv
from decimal import Decimal
import os
from types import NoneType
from client_column_transforms import column_name_mappings

# Data type validators
def is_decimal(data):
    return isinstance(data, Decimal)

def is_decimal_nullable(data):
    return isinstance(data, (Decimal, NoneType))

def is_int_nullable(data):
    return isinstance(data, (int, NoneType))

def is_string(data):
    return isinstance(data,str)


# Read column names (header)
class MerchantDataFileHandler:

    def __init__(self, multiply_merchant_id):
        self.multiply_merchant_id = multiply_merchant_id  

        #Raise an error if the multiply_merchant_id doesnot exist
        if multiply_merchant_id not in column_name_mappings:
            raise ValueError('multiply_merchant_id does not exist')

        self.file_path = os.path.join('.', 'data', "{multiply_merchant_id:}_product_update.csv".format(multiply_merchant_id=multiply_merchant_id))
        self.column_name_mapping = column_name_mappings[multiply_merchant_id]
        
    

        # TODO: Add more column validators and 
        # data transformers as appropriate

        self.column_data_validators = {
            'merchant_product_id': [is_string,],
            'marketplace_product_id': [is_string,],
            'name': [is_string,],
            'max_price_inc_vat': [is_decimal],
            'min_price_inc_vat': [is_decimal_nullable],
            'stock_qty':[is_int_nullable]
            # validators
        }

        self.column_data_transformers = {
            'merchant_product_id': [str,],
            'marketplace_product_id': [str,],
            'name': [str,],
            'max_price_inc_vat': [Decimal,],
            'min_price_inc_vat': [Decimal,],
            'stock_qty':[int]
            # data transformers
        }

    
    def generate_output_file_contents(self):
        # 1. read input file
        # 2. validate data
        # 3. create output contents (inject multiply merchant id here)
        out_rows = []
        err_rows = []

        # read data

        with open(self.file_path, 'r') as inputFile:
            reader = csv.reader(inputFile, delimiter=',')
            header = next(reader) # the header row is skipped
            rows = []
            for i in reader:
                rows.append(i)


            #map headers

            for index,i in enumerate(header):
                if i in self.column_name_mapping:
                    header[index] = self.column_name_mapping[i]

            products = []
            #loops through each row and check if all the values have valid types if not it transforms it to the approppriate data type and re attaches it back to the dictionary
            for i in rows:
                myDict = {}
                for index, j in enumerate(i):
                    #validate data
                    if header[index] in self.column_data_validators:
                        types = self.column_data_validators[header[index]]

                        for k in types:

                            if k(j) is False: 
                                if header[index] in self.column_data_transformers:
                                    for t in self.column_data_transformers[header[index]]:
                                        j = t(j)
                    myDict[header[index]] = j

                products.append(myDict)
                print(products)

    #set the multiply_merchant_id if it is not found in the columns
            for index, i in enumerate(products):
                if 'multiply_merchant_id' not in i:
                    i['multiply_merchant_id'] = self.multiply_merchant_id
                    products[index] = i

            out_rows = products

            inputFile.close()

        return  out_rows, err_rows
