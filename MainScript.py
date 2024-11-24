## import required packages
import selenium
import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

## define chrome driver and option arguments
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
chromeDriver = webdriver.Chrome(options=options)

def CheckIf_ElementExists(xpath):
    try:
        chromeDriver.find_element(By.XPATH,xpath)
        return True
    except Exception:
        return False

def Wait_till_ElementVisible(_xpath):
    a = 1
    try:
        while(a < 300):
            if(CheckIf_ElementExists(_xpath)):
                return True
                break
            a += 1
    except Exception:
        return False

url = "https://www.fitpeo.com/"

menuPath = "//*[@data-testid='MenuIcon']"
revCalPath = "//*[contains(@class,'MuiListItemText')][contains(text(),'Revenue Calculator')]"
sliderPath = "//*[contains(@class,'MuiSlider')]"
inputfacyPath = "//*[@type='number'][contains(@class,'MuiInputBase-input')]"

## login to website
chromeDriver.get(url)
Wait_till_ElementVisible(menuPath)
chromeDriver.find_element(By.XPATH,menuPath).click()
time.sleep(2)
chromeDriver.find_element(By.XPATH,revCalPath).click()
time.sleep(2)
Wait_till_ElementVisible(sliderPath)
## scroll to element
chromeDriver.execute_script("arguments[0].scrollIntoView();", chromeDriver.find_element(By.XPATH,sliderPath))
time.sleep(2)

## select/enter facility rate number
# print("Please Enter the Facility Rate:\n")
inputFacilityRate = "560" #input()
enterInputFacyRate = chromeDriver.find_element(By.XPATH,inputfacyPath)
enterInputFacyRate.clear()
enterInputFacyRate.send_keys(Keys.CONTROL + 'a')
enterInputFacyRate.send_keys(inputFacilityRate)
time.sleep(2)

## select/enter list of cpt codes
# print("Please Provide the CPT Codes with Comma (,) seperated:")
cptList = []
inputCPTs =  "99091,99453,99454,99474" #input()
cptList = inputCPTs.split(",")

#slecting cpt codes
cptCode = ""
for cptCode in cptList:
    cptPath = "//*[contains(text(),'CPT-"+cptCode+"')]/ancestor::div[1]/label//input"
    Wait_till_ElementVisible(cptPath)
    chromeDriver.execute_script("arguments[0].scrollIntoView();", chromeDriver.find_element(By.XPATH,cptPath))
    time.sleep(1)
    ## select checkboxes
    chromeDriver.find_element(By.XPATH,cptPath).click()
    time.sleep(1)

## print the required data
try:
    GrossAmount = chromeDriver.find_element(By.XPATH,"//*[contains(text(),'Total Gross Revenue Per Year')]/ancestor::div[1]/h3").text
    IndividualPatient = chromeDriver.find_element(By.XPATH,"//*[contains(text(),'Total Individual Patient/Month')]/ancestor::div[1]/p[2]").text
    RecurReimbursement = chromeDriver.find_element(By.XPATH,"//*[contains(text(),'Total Recurring Reimbursement for all Patients Per Month')]/ancestor::div[1]/p[2]").text
    OneTimeReimbursement  = chromeDriver.find_element(By.XPATH,"//*[contains(text(),'One Time Reimbursement for all Patients Annually')]/ancestor::div[1]/p[2]").text

    print("Facility Rate: " + inputFacilityRate)
    print("CPT Codes: " + inputCPTs)
    print("Total Individual Patient/Month: " + IndividualPatient)
    print("Total Recurring Reimbursement for all Patients/Month: " + RecurReimbursement)
    print("One Time Reimbursement for all Patients Anually: " + OneTimeReimbursement)
    print("Total Gross Revenue/Year: " + GrossAmount)
except Exception:
    print("Unexpected Error")

## close and quite the driver instance
chromeDriver.close()
chromeDriver.quit()
