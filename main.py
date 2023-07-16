import csv
import json
import os
import string
import time

from selenium import webdriver
import webbrowser

from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def login(username, password, driver):
    driver.get('https://ges-cas.kordis.fr/login?service=https%3A%2F%2Fmyges.fr%2Fj_spring_cas_security_check')

    wait = WebDriverWait(driver, 10)

    username_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
    password_input = wait.until(EC.presence_of_element_located((By.ID, 'password')))
    submit_button = wait.until(EC.element_to_be_clickable((By.NAME, 'submit')))

    username_input.send_keys(username)
    password_input.send_keys(password)
    submit_button.click()

    scrape_notes(driver)


def scrape_notes(driver):
    # Récupérer les notes
    driver.get('https://myges.fr/student/home')

    wait = WebDriverWait(driver, 5)

    scolarite_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="mg_menu_texte"]')))
    ActionChains(driver).move_to_element(scolarite_element).click().perform()

    notes_element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Notes et absences')]")))
    notes_element.click()

    select_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'marksForm:j_idt174:periodSelect')))
    select_element.click()

    sem2_element = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="marksForm:j_idt174:periodSelect_panel"]/div/ul/li[2]')))
    driver.execute_script("arguments[0].scrollIntoView();", sem2_element)
    sem2_element.click()

    time.sleep(5)
    marksS2 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'marksForm:marksWidget:coursesTable')))
    marksS2_txt = marksS2.text
    s2 = [marksS2_txt]
    # print(s2)
    # writeFiles(s2)
    select_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'marksForm:j_idt174:periodSelect')))
    select_element.click()


    sem1_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="marksForm:j_idt174:periodSelect_panel"]/div/ul/li[3]')))
    sem1_element.click()

    time.sleep(5)
    marksS1 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'marksForm:marksWidget:coursesTable')))
    marksS1_txt = marksS1.text
    s1 = [marksS1_txt]
    file = s1 + ["\n"] + s2
    print(file)
    writeFiles(file)


def scrape_emploi(driver):
    driver.get('https://myges.fr/student/home')
    emploi_element = driver.find_element(By.XPATH, '//*[@id="mg_portal_nav"]/li[3]/a')
    emploi = emploi_element.click()
    planning = []
    planning_element_days = driver.find_elements(By.CSS_SELECTOR, 'label#calendar\\:currentWeek')
    planning_element_hours = driver.find_elements(By.XPATH, '//*[@id="calendar:myschedule_container"]/div/div/div/div'
                                                            '/div/table')
    dates_element = driver.find_element(By.CSS_SELECTOR, 'label#calendar\\:currentWeek')
    dates_text = dates_element.text
    # for i in range(len(planning_element_days)):
    #     planning = planning_element_days[i].find_elements()
    print(dates_text)
    return emploi



def writeFiles(fileType):
    filename = "exportFiles/note.csv"
    translator = str.maketrans("", "", string.punctuation)

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for row in fileType:
            cleaned_row = row.translate(translator)
            writer.writerow([cleaned_row])


if __name__ == '__main__':
    DRIVER_PATH = Service(r'D:\googleDriver\chromedriver.exe')
    driver = webdriver.Chrome(service=DRIVER_PATH)
    username = 'arasiah'
    password = '5hdMVY3Q'
    login(username, password, driver)

    driver.quit()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
