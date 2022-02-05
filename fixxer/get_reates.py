import tkinter     # import tkinter for create popup window
import json  # import json module
import requests     # import requests library
from tkinter import Entry, messagebox   # import messagebox for show error or information
## this dictionary for parameters of rules 
rules = {
    "archive": True ,
    "filter" : False ,
    "prefered" : ["BTC", "IRR", "USD"],
    "token" : "a3729cef26bf542ec4989669629d1d9d",
    "url" : "http://data.fixer.io/api/latest?access_key=" ,
    "popup" : True,
    "currency" : "",
    "optimal" : 2
}
archivepath = "/home/armin/Desktop/project/convert_file_types/test/archive.json"    # set path of archive file

def check_rules(rules):
    """
    check rules for valid or not
    """
    if rules['token'] == '':
        messagebox.showerror('Error', 'Please enter token')
        return False
    if rules['url'] == '':
        messagebox.showerror('Error', 'Please enter url')
        return False
    if rules['filter'] and rules['prefered'] == []:
        messagebox.showerror('Error', 'Please enter prefered currency')
        return False
    return True

def get_data(url, token):
    """
    get data from fixer.io
    and make json file for archive or not 
    and check filter is enable or not if enable check prefered currency
    return data (dictionary that make) 
    """
    response = requests.get(url + token)
    rates = dict()
    if response.status_code == 200 and response.json()['success']:
        if rules['filter']:
            for key in rules['prefered']:
                if key in response.json()['rates']:
                    rates[key] = response.json()['rates'][key]
        else:
            rates = response.json()['rates']   
    return rates
def archiving(archivepath):
    """
    archiving data from fixer.io
    check the flag of archive in rules is true or false if true make json file
    """
    if rules['archive']:
        with open(archivepath, 'w', encoding='utf_8') as archivereader:
            archivereader.write(json.dumps(get_data(rules['url'], rules['token']), indent=0))


def notif():
    """
    create popup if the cost of the currency is less than the cost of the prefered currency
    """
    if rules['popup']:
        data = get_data(rules['url'], rules['token'])   
        try:
            if data[rules['currency']] < rules['optimal']:   # check the cost of the currency is less than the cost of the prefered currency
                messagebox.showinfo('Information', 'The cost of the currency is less than the cost of the prefered currency') 
        except:     # if the currency is not in the rules of currency
            popup = tkinter.Tk()     # create popup window for show user to enter currency
            popup.title('Enter your currency')   # set title of popup window
            popup.geometry('300x100')   # set size of popup window
            namevalue = tkinter.StringVar()    # create variable for store value of currency
            Entry(popup, textvariable=namevalue).pack()     # create entry for user to enter currency
            # namevalue.set('Enter your currency')    # set default value of currency
            def on_click():
                currency = namevalue.get()  # get value from entry
                if currency in data:
                    rules['currency'] = currency    # set value of currency in rules
                    popup.destroy()     # destroy popup window
                    popup.quit()    # close popup window
                    notif()  # call function notif()
            tkinter.Button(popup, text='OK', command=on_click).pack()    # create button for user to click   and call on_click function
            popup.mainloop()

if __name__ == '__main__':
    notif()
    check_rules(rules)