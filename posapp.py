import kivy
kivy.require("1.9.1")
import inventory
from local_time import DATE as DATE
import thread
import csv
from time import sleep
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton

Inventory = inventory.Inventory()
itembutton_dict = {}


Builder.load_file('pos.kv', rulesonly = True)

### callbacks ###
def callback1(self):
    item = self.id
    Inventory.add_to_cart(item)
    Cartlabel.text = 'Cart has ' + str(len(Inventory.cartitem_list))

def add_from_text(self):
    item = Textinput.text
    if item in Inventory.item_id:
        Inventory.add_to_cart(item)
        Cartlabel.text = 'Cart has ' + str(len(Inventory.cartitem_list))
    else:
        Cartlabel.text = 'Error\nItem has no Match'

def callback2(self):
    if self.text == 'Home':
        sm.current = 'home'
    elif self.text == 'Back':
        sm.current = 'sales'
    else:
        sm.current = self.id

def remove(self):
    item = self.id.strip()
    Inventory.remove_from_cart(item)
    cartbuilder(self)
    Cartlabel.text = 'Cart has ' + str(len(Inventory.cartitem_list))

def clear(self):
    Inventory.cartitem_list =[]
    Inventory.cartcount_dict = {}
    Inventory.priceadjust = 0
    cartpopup.dismiss()
    discountlabel.text = str(Inventory.priceadjust)
    Cartlabel.text = 'Cart has ' + str(len(Inventory.cartitem_list))


def submit(self):
    for item in Inventory.cartitem_list:
        Inventory.remove_stock(item)
        print item + 'inventory change to: ' + Inventory.inventory_dict[item]
        btntext = Inventory.name_dict[item] + '\nStock: ' + str(Inventory.inventory_dict[item])  
        btn = itembutton_dict[item]
        btn.text = btntext
    Inventory.add_sale()
    clear(self)

def editprice(self):
    try:
        amount = int(priceinput.text)
        if self.text == '+':
            Inventory.priceadjust += amount
        elif self.text == '-':
            Inventory.priceadjust -= amount
        priceinput.text = ''
        discountlabel.text = str(Inventory.priceadjust)
        cartbuilder(self)
    except:
        cartmessage.text = 'Price Adjustment must be a number with no decimals'

def cartbuilder(self):
    cartitems.clear_widgets()
    keys = Inventory.cartcount_dict.keys()
    subtotal = 0.0
    itemtotal = 0.0
    for i in keys:
        cartitems.add_widget(Label(text = str(Inventory.cartcount_dict[i]), size_hint_y = None, height = 30))
        cartitems.add_widget(Label(text = Inventory.name_dict[i] + ', ' + Inventory.category_dict[i], size_hint_y = None, height = 30))
        cartitems.add_widget(Label(text = '@' + Inventory.price_dict[i][Inventory.setchannel], size_hint_y = None, height = 30))
        cartitems.add_widget(Label(text = str(float(Inventory.price_dict[i][Inventory.setchannel]) * Inventory.cartcount_dict[i]), size_hint_y = None, height = 30))        
        removebtn = Button(text = 'Remove', id = ' ' + i + ' ', size_hint_y = None, height = 30)
        removebtn.bind(on_release = remove)
        cartitems.add_widget(removebtn)
        itemtotal = float(Inventory.price_dict[i][Inventory.setchannel]) * Inventory.cartcount_dict[i]
        subtotal += itemtotal
    subtotal += Inventory.priceadjust
    cartitems.add_widget(Label(text = '', size_hint_y = None, height = 30)) # blank bloc
    cartitems.add_widget(Label(text = '', size_hint_y = None, height = 30)) # blank bloc
    cartitems.add_widget(Label(text = 'Total:', size_hint_y = None, height = 30))
    cartitems.add_widget(Label(text = str(subtotal), size_hint_y = None, height = 30))
    cartitems.add_widget(Label(text = '', size_hint_y = None, height = 30)) # blank bloc
    
def changechannel(self):
    Inventory.setchannel = self.text
    cartpopup.title = 'Cart - '+ Inventory.setchannel
    channelpopup.dismiss()
    cartbuilder(self)

def itemfind(key):
    item = str(key)
    if item in Inventory.item_id:
        IteminfoLayout.clear_widgets()
        namelabel = Label(text = 'Name:  ' + Inventory.name_dict[item])
        IteminfoLayout.add_widget(namelabel)
        catlabel = Label(text = 'Category:  ' + Inventory.category_dict[item])
        IteminfoLayout.add_widget(catlabel)
        stocklabel = Label(text = 'Stock Type:  ' + Inventory.stocktype_dict[item])
        IteminfoLayout.add_widget(stocklabel)
        inventorylabel = Label(text = 'Inventory:  ' + str(Inventory.inventory_dict[item]))
        IteminfoLayout.add_widget(inventorylabel)
        IteminfoLayout.add_widget(closebutton)
        Iteminfopopup.title = item
        Iteminfopopup.open()
    else:
        print item
def callback3(self):
    pass

class HomeScreen(Screen):
    pass
class CategoryGrid(GridLayout):
    pass

sm = ScreenManager()
sm.add_widget(HomeScreen(name='home'))



### cart popup code ###
cartcontent = BoxLayout(orientation = 'vertical')
cartitems = GridLayout(cols =5)
cartcontent.add_widget(cartitems)

editpricebox = BoxLayout(size_hint_y = None, height = 30)
cartcontent.add_widget(editpricebox)
priceinput = TextInput(text = '0', multiline = False)
editpricebox.add_widget(priceinput)
plusbtn = Button(text = '+')
plusbtn.bind(on_release = editprice)
editpricebox.add_widget(plusbtn)
minusbtn = Button(text = '-')
minusbtn.bind(on_release = editprice)
editpricebox.add_widget(minusbtn)
editpricebox.add_widget(Label(text = 'Price Adjust:'))
discountlabel = Label(text = '0')
editpricebox.add_widget(discountlabel)

cartbuttons = BoxLayout(size_hint_y = None, height = 80)
cartcontent.add_widget(cartbuttons)
closecart = Button(text = 'Close Cart')
cartbuttons.add_widget(closecart)
clearcart = Button(text = 'Clear Cart')
cartbuttons.add_widget(clearcart)
submitcart = Button(text = 'Submit')
cartbuttons.add_widget(submitcart)
channelchange = Button(text = 'Change\nChannel')
cartbuttons.add_widget(channelchange)
cartpopup = Popup(title = 'Cart - Default', content = cartcontent)
cartpopup.bind(on_open = cartbuilder)
closecart.bind(on_press = cartpopup.dismiss)
clearcart.bind(on_press = clear)
submitcart.bind(on_press= submit)
cartmessage = Label(text = 'system messages', size_hint_y = None, height = 30)
cartcontent.add_widget(cartmessage)

### sales Channel ### complete callback
channelbuttons = BoxLayout(orientation = 'vertical')
channelpopup = Popup(title = 'Sales Channel',content = channelbuttons, size_hint_x = None, width = 200)
for i in Inventory.saleschannel_list:
    toggle = ToggleButton(text = i, group = 'channels')
    toggle.bind(on_press = changechannel)
    channelbuttons.add_widget(toggle)

channelchange.bind(on_press = channelpopup.open)    


### sales screen ###
SalesScreen = Screen(name = 'sales')
SalesLayout = BoxLayout(orientation = 'vertical')
SalesScreen.add_widget(SalesLayout)
SalesGrid = GridLayout(cols =5)
SalesLayout.add_widget(SalesGrid)
IteminputBox = BoxLayout(size_hint_y = .08)
SalesLayout.add_widget(IteminputBox)
Textinput = TextInput(text =  'Input Item ID', multiline = False)
IteminputBox.add_widget(Textinput)
Textbtn = Button(text = 'Add', size_hint_x = .3)
Textbtn.bind(on_release = add_from_text)
IteminputBox.add_widget(Textbtn)
SalesLayoutBottom = BoxLayout(size_hint_y = .15)
SalesLayout.add_widget(SalesLayoutBottom)
Cartbtn = Button(text = 'Cart')
Cartbtn.bind(on_press = cartpopup.open)
Homebtn = Button(text = 'Home')
Homebtn.bind(on_release = callback2)
Cartlabel = Label(text = '0 items in cart')
SalesLayoutBottom.add_widget(Cartlabel)
SalesLayoutBottom.add_widget(Homebtn)
SalesLayoutBottom.add_widget(Cartbtn)
sm.add_widget(SalesScreen)

for cat in Inventory.category_list:
    newscn = Screen(name = cat)
    sm.add_widget(newscn)
    btn = Button(text = cat, id = cat)
    btn.bind(on_press = callback2)
    SalesGrid.add_widget(btn)

    ItemGrid = GridLayout(cols = 5, size_hint_y = None)
    ItemGrid.bind(minimum_height = ItemGrid.setter('height'))
    
    ItemGrid.add_widget(Label(text = cat,size_hint_y = None, height = 100))
    ItemGrid.add_widget(Label(text = ' ',size_hint_y = None, height = 100))

    backbtn = Button(text = 'Back', id = 'back', size_hint_y = None, height = 100)
    backbtn.bind(on_press = callback2)
    ItemGrid.add_widget(backbtn)
    cartbtn = Button(text = 'Cart', id = 'cart', size_hint_y = None, height = 100)
    cartbtn.bind(on_press = cartpopup.open)
    ItemGrid.add_widget(cartbtn)

    homebtn = Button(text = 'Home', id = 'home', size_hint_y = None, height = 100)
    homebtn.bind(on_press =callback2)
    ItemGrid.add_widget(homebtn)

    ItemGrid.add_widget(Label(text = '',size_hint_y = None, height = 10)) 
    ItemGrid.add_widget(Label(text = '',size_hint_y = None, height = 10))
    ItemGrid.add_widget(Label(text = '',size_hint_y = None, height = 10))
    ItemGrid.add_widget(Label(text = '',size_hint_y = None, height = 10))
    ItemGrid.add_widget(Label(text = '',size_hint_y = None, height = 10))

    itemlist = []
    sortlist = {}
    for ID in Inventory.item_id:
        itemcategory = Inventory.category_dict[ID]
        if cat == itemcategory:
            sortlist[ID] = Inventory.name_dict[ID]
    presorted = sorted(sortlist.items(), key = lambda (k,v): v)
    for i in presorted:
        itemlist.append(i[0])
    for ID in itemlist:
        btntext = Inventory.name_dict[ID] + '\nStock: ' + str(Inventory.inventory_dict[ID])  
        btn = Button(text = btntext, id = ID, size_hint_y = None, height = 80)
        itembutton_dict[ID] = btn
        btn.bind(on_press = callback1)
        ItemGrid.add_widget(btn)
    scrollview = ScrollView()
    scrollview.add_widget(ItemGrid)
    newscn.add_widget(scrollview)



IteminfoLayout = BoxLayout(orientation = 'vertical')
Iteminfopopup = Popup(title = 'Item', content = IteminfoLayout, size_hint=(None,None), height = 500, width = 400)
namelabel = Label(text = 'Name:  ')
IteminfoLayout.add_widget(namelabel)
catlabel = Label(text = 'Category:  ')
IteminfoLayout.add_widget(catlabel)
stocklabel = Label(text = 'Stock Type:  ')
IteminfoLayout.add_widget(stocklabel)
inventorylabel = Label(text = 'Inventory:  ')
IteminfoLayout.add_widget(inventorylabel)
closebutton = Button(text = 'Close')
closebutton.bind(on_press = Iteminfopopup.dismiss)
IteminfoLayout.add_widget(closebutton)


    
class POSApp(App):
    def build(self):
        return sm        
    def on_stop(self):
        Inventory.subtract_inventory()

