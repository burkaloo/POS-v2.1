import csv
from local_time import DATE as DATE

class Inventory(object):

    def __init__(self):
        self.item_id = []
        self.category_list = []
        self.category_dict = {}
        self.name_dict = {}
        self.price_dict ={}
        self.inventory_dict = {}
        self.category_count = 0
        self.stocktype_dict = {}
        self.discount_dict = {}
        self.cartitem_list = []
        self.cartcount_dict = {}
        self.order_num = 00000
        self.imported = False
        self.saleschannel_list = []
        self.priceadjust = 0
        self.setchannel = 'Default'

        self.col_labels = ['Order#',
                           'DATE SOLD',
                           'ITEM ID',
                           'CATEGORY',
                           'NAME',
                           'PRICE SOLD',
                           'QTY',
                           'STOCK TYPE',
                           'DISCOUNT PROMO',
                           'CHANNEL']
        if self.imported == False:
            self.start()
            self.imported = True

    def import_from_csv(self):
        inventory_file = open('inventory.csv', 'r')
        csv_read = csv.reader(inventory_file)
        DATA = list(csv_read)

        for i in range(6):
            del DATA[0][0]
            self.saleschannel_list = DATA[0]
        
        print DATA[0]
        del DATA[0]

        for i in DATA:
            self.item_id.append(i[0])
            self.category_dict[i[0]] = i[1]
            self.name_dict[i[0]] = i[2]
            self.inventory_dict[i[0]] = int(i[3])
            self.stocktype_dict[i[0]] = i[4]
            self.discount_dict[i[0]] = i[5]
            self.price_dict[i[0]] = {}
            Dataindex = 6
            for x in self.saleschannel_list:
                less = 1 - float(i[5])
                price = float(i[Dataindex]) * less
                self.price_dict[i[0]][x] = str(price)
                Dataindex += 1
            
        print 'Import Complete'
        inventory_file.close()

        salestodate_file = open('sales_to_date.csv', 'r')
        salestodate = list(csv.reader(salestodate_file))
        try:
            self.order_num = int(salestodate[-1][0]) + 1
        except:
            self.order_num = 00001
        print self.order_num
        salestodate_file.close()
            

    def count_categories(self):
        for i in self.item_id:
            if self.category_dict[i] in self.category_list:
                continue
            else:
                self.category_list.append(self.category_dict[i])
        print self.category_list
        self.category_count = len(self.category_list)
        print 'DATA has ', self.category_count, ' Categories'
        
    def start(self):
        self.commit_salestoday()
        self.import_from_csv()
        self.count_categories()

    def add_to_cart(self,obj):
        if self.inventory_dict[obj] > 0:
            if obj in self.cartitem_list:
                if self.cartcount_dict[obj] < self.inventory_dict[obj]:
                    self.cartcount_dict[obj] += 1
            else:
                self.cartcount_dict[obj] = 1
            self.cartitem_list.append(obj)
        
    def remove_from_cart(self, obj):
        self.cartitem_list.remove(obj)
        if self.cartcount_dict[obj] == 1:
            del self.cartcount_dict[obj]
        else:
            self.cartcount_dict[obj] -= 1

    def commit_salestoday(self):
        salestodate_file = open('sales_to_date.csv', 'a')
        writer = csv.writer(salestodate_file, lineterminator = '\n')
        salestoday_file = open('sales_today.csv','r')
        writelist = list(csv.reader(salestoday_file))
        salestoday_file.close()
        del writelist[0]
        if len(writelist) != 0:
            for i in writelist:
                writer.writerow(i)
            self.clear_salestoday()
        salestodate_file.close()

    def clear_salestoday(self):
        salestoday_file = open('sales_today.csv', 'w')
        writer = csv.writer(salestoday_file, lineterminator = '\n')
        writer.writerow(self.col_labels)
        salestoday_file.close()

    def remove_stock(self, obj):
        key = obj
        stock = self.inventory_dict[key]
        stock -= 1
        self.inventory_dict[key] = stock
        
    def add_sale(self):
        salestoday_file = open('sales_today.csv', 'a')
        writer = csv.writer(salestoday_file, lineterminator = '\n')
        keys = self.cartcount_dict.keys()
        print 'keys', keys
        for i in keys:
            row = [self.order_num,                       # Order num
                   DATE,                                 # Date sold
                   i,                                    # Item num 
                   self.category_dict[i],                # Item category
                   self.name_dict[i],                    # Item name
                   self.price_dict[i][self.setchannel],  # Item price today
                   self.cartcount_dict[i],               # Qty sold
                   self.stocktype_dict[i],               # Item stock type
                   self.discount_dict[i],                # item discount rate today
                   self.setchannel]                      # Sales Channel
            writer.writerow(row)
        if self.priceadjust != 0:
            writer.writerow([self.order_num, DATE, '', '', 'Price Adjust', self.priceadjust])
        self.order_num +=1
        salestoday_file.close()
        print 'sale recorded'

    def subtract_inventory(self):
        print 'sub start'
        salestoday_file = open('sales_today.csv', 'r')
        saleslist = list(csv.reader(salestoday_file))
        salestoday_file.close()
        del saleslist[0]
        if len(saleslist) != 0:
            inventory_file = open('inventory.csv', 'w')
            writer = csv.writer(inventory_file, lineterminator = '\n')
            row = ['ITEM ID', 'CATEGORY', 'NAME', 'INVENTORY', 'STOCK TYPE', 'DISCOUNT']
            row.extend(self.saleschannel_list)
            writer.writerow(row)
            self.item_id.sort()
            for i in self.item_id:
                row = [i,
                       self.category_dict[i],
                       self.name_dict[i],
                       self.inventory_dict[i],
                       self.stocktype_dict[i],
                       self.discount_dict[i]]
                for x in self.saleschannel_list:
                    row.append(self.price_dict[i][x])
                writer.writerow(row)
            inventory_file.close()
            print 'inventory edited'
        else:
            print 'No inventory Change'
        print 'sub end'
        
