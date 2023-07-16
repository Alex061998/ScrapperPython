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
from urllib3.filepost import writer


def login(username, password, driver):
    driver.get('https://ges-cas.kordis.fr/login?service=https%3A%2F%2Fmyges.fr%2Fj_spring_cas_security_check')

    wait = WebDriverWait(driver, 10)

    username_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
    password_input = wait.until(EC.presence_of_element_located((By.ID, 'password')))
    submit_button = wait.until(EC.element_to_be_clickable((By.NAME, 'submit')))

    username_input.send_keys(username)
    password_input.send_keys(password)
    submit_button.click()
    # scope_Trobinoscoupe_Etudiant(driver)
    scrape_notes(driver)


def scrape_notes(driver):
    # Récupérer les notes
    driver.get('https://myges.fr/student/home')

    wait = WebDriverWait(driver, 5)

    scolarite_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="mg_menu_texte"]')))
    ActionChains(driver).move_to_element(scolarite_element).click().perform()

    notes_element = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Notes et absences')]")))
    notes_element.click()

    select_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'marksForm:j_idt174:periodSelect')))
    select_element.click()

    sem2_element = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="marksForm:j_idt174:periodSelect_panel"]/div/ul/li[2]')))
    driver.execute_script("arguments[0].scrollIntoView();", sem2_element)
    sem2_element.click()

    time.sleep(5)
    marksS2 = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, 'marksForm:marksWidget:coursesTable')))
    marksS2_txt = marksS2.text
    s2 = [marksS2_txt]
    # print(s2)
    # writeFiles(s2)
    select_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'marksForm:j_idt174:periodSelect')))
    select_element.click()

    sem1_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="marksForm:j_idt174:periodSelect_panel"]/div/ul/li[3]')))
    sem1_element.click()

    time.sleep(5)
    marksS1 = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, 'marksForm:marksWidget:coursesTable')))
    marksS1_txt = marksS1.text
    s1 = [marksS1_txt]
    file = s1 + ["\n"] + s2
    print(file)
    writeFilesForNotes(file)


def scope_Trobinoscoupe_Etudiant(driver):
    driver.get('https://myges.fr/student/home')

    wait = WebDriverWait(driver, 5)

    etudiant_menu = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="mg_menu_texte"]')))
    ActionChains(driver).move_to_element(etudiant_menu).click().perform()

    etudiants_element = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Trombinoscope étudiants')]")))
    etudiants_element.click()

    time.sleep(5)

    # trobi_etudiant = wait.until(
    #     EC.presence_of_element_located((By.XPATH, '//*[@id="studentDirectoryWidget:studentDirectoryDataGrid_content"]')))

    name_elements = driver.find_elements(By.XPATH, '//div[@class="mg_directory_text"]')

    # Extract the student names
    student_names = []
    for name_element in name_elements:
        name = name_element.text.strip()
        student_names.append(name)

    if len(name_elements) == 15:
        paginator = driver.find_element(By.XPATH,
                                        '//*[@id="studentDirectoryWidget:studentDirectoryDataGrid_paginator_bottom"]/span[3]/span[2]')
        paginator.click()
        time.sleep(2)
        name_elements = driver.find_elements(By.XPATH, '//div[@class="mg_directory_text"]')
        for name_element in name_elements:
            name = name_element.text.strip()
            student_names.append(name)
    time.sleep(5)
    writeFilesForTrobiScopeEleveOnly3Al(student_names)

    ### For 3rd Logicel Classes

    logiciel_element = driver.find_element(By.XPATH, '//*[@id="puidOptions"]/tbody/tr/td[3]/div/div[2]')
    logiciel_element.click()

    time.sleep(2)

    logicielClass_element = driver.find_elements(By.XPATH, '//div[@class="mg_directory_text"]')

    # Extract the student names
    studentLogiciel_names = []
    for name_element in logicielClass_element:
        name = name_element.text.strip()
        studentLogiciel_names.append(name)

    if len(logicielClass_element) == 15:
        paginator = driver.find_element(By.XPATH,
                                        '//*[@id="studentDirectoryWidget:studentDirectoryDataGrid_paginator_bottom"]/span[3]/span[2]')
        paginator.click()
        time.sleep(2)
        name_elements = driver.find_elements(By.XPATH, '//div[@class="mg_directory_text"]')
        for name_element in name_elements:
            name = name_element.text.strip()
            studentLogiciel_names.append(name)

    # if len(logicielClass_element) == 31:
    #     paginator = driver.find_element(By.XPATH,
    #                                     '//*[@id="studentDirectoryWidget:studentDirectoryDataGrid_paginator_bottom"]/span[3]/span[2]')
    #     paginator.click()
    #     time.sleep(2)
    #     name_elements = driver.find_elements(By.XPATH, '//div[@class="mg_directory_text"]')
    #     for name_element in name_elements:
    #         name = name_element.text.strip()
    #         studentLogiciel_names.append(name)
    time.sleep(5)
    writeFilesForTrobiScopeEleveOnlyEveryone(studentLogiciel_names)


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


def writeFilesForTrobiScopeEleveOnly3thClasses(file):
    filename = "exportFiles/trobiEleveOnly3thClasses.csv"
    translator = str.maketrans("", "", string.punctuation)

    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        for row in file:
            cleaned_row = row.translate(translator)
            writer.writerow([cleaned_row])


def writeFilesForTrobiScopeEleveOnlyEveryone(file):
    filename = "exportFiles/trobiEleveEveryone.csv"
    translator = str.maketrans("", "", string.punctuation)

    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        for row in file:
            cleaned_row = row.translate(translator)
            writer.writerow([cleaned_row])


def writeFilesForTrobiScopeEleveOnly3Al(file):
    filename = "exportFiles/trobiEleve3al.csv"
    translator = str.maketrans("", "", string.punctuation)

    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        for row in file:
            cleaned_row = row.translate(translator)
            writer.writerow([cleaned_row])


def writeFilesForNotes(fileType):
    filename = "exportFiles/note.txt"
    # translator = str.maketrans("", "", string.punctuation)

    with open(filename, 'w') as file:
        for row in fileType:
            file.write(row + '\n')


if __name__ == '__main__':
    DRIVER_PATH = Service(r'D:\googleDriver\chromedriver.exe')
    driver = webdriver.Chrome(service=DRIVER_PATH)
    username = 'arasiah'
    password = '5hdMVY3Q'
    login(username, password, driver)

    driver.quit()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
