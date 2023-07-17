import csv
import json
import os
import string
import time

import uvicorn as uvicorn
from selenium import webdriver
import webbrowser

from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib3.filepost import writer

from api import app


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
    # scrape_notes(driver)


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
    # writeFilesForNotes(file)


def scopeAllStudentOf3rdClass(driver):
    logiciel_element = driver.find_element(By.XPATH, '//*[@id="puidOptions"]/tbody/tr/td[5]/div/div[2]/span')
    logiciel_element.click()
    time.sleep(2)

    studentLogiciel_names = []
    page_number = 0
    while True:
        xpath_expression = '//*[@id="studentDirectoryWidget:studentDirectoryDataGrid_paginator_bottom"]/span[3]/span[' \
                           'count(preceding-sibling::span) >= ' + str(page_number) + ']'
        try:
            paginator = driver.find_element(By.XPATH, xpath_expression)
        except NoSuchElementException:
            break  # Break out of the loop if paginator element is not found
        paginator.click()
        time.sleep(5)
        logicielClass_element = driver.find_elements(By.XPATH, '//div[@class="mg_directory_text"]')
        for name_element in logicielClass_element:
            name = name_element.text.strip()
            studentLogiciel_names.append(name)
        print(len(studentLogiciel_names), "1")
        time.sleep(2)
        page_number += 1
    time.sleep(5)
    writeFilesForTrobiScopeEleveOnlyEveryone(studentLogiciel_names)


def scope_Trobinoscoupe_Etudiant(driver):
    driver.get('https://myges.fr/student/home')

    wait = WebDriverWait(driver, 5)

    etudiant_menu = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="mg_menu_texte"]')))
    ActionChains(driver).move_to_element(etudiant_menu).click().perform()

    etudiants_element = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Trombinoscope étudiants')]")))
    etudiants_element.click()

    time.sleep(5)

    # Extract the student names
    studentLogiciel_names = []
    page_number = 0
    while True:
        xpath_expression = '//*[@id="studentDirectoryWidget:studentDirectoryDataGrid_paginator_bottom"]/span[3]/span[' \
                           'count(preceding-sibling::span) >= ' + str(page_number) + ']'
        try:
            paginator = driver.find_element(By.XPATH, xpath_expression)
        except NoSuchElementException:
            break  # Break out of the loop if paginator element is not found
        paginator.click()
        time.sleep(5)
        logicielClass_element = driver.find_elements(By.XPATH, '//div[@class="mg_directory_text"]')
        for name_element in logicielClass_element:
            name = name_element.text.strip()
            studentLogiciel_names.append(name)
        print(len(studentLogiciel_names), "1")
        time.sleep(2)
        page_number += 1
    time.sleep(5)

    writeFilesForTrobiScopeEleveOnly3Al(studentLogiciel_names)

    # getAllStudentOfAL(driver)
    # scopeAllStudentOf3rdClass(driver)


def getAllStudentOfAL(driver):
    ### For 3rd Logicel Classes
    logiciel_element = driver.find_element(By.XPATH, '//*[@id="puidOptions"]/tbody/tr/td[3]/div/div[2]')
    logiciel_element.click()
    time.sleep(2)

    # Extract the student names
    studentLogiciel_names = []
    page_number = 0
    while True:
        xpath_expression = '//*[@id="studentDirectoryWidget:studentDirectoryDataGrid_paginator_bottom"]/span[3]/span[' \
                           'count(preceding-sibling::span) >= ' + str(page_number) + ']'
        try:
            paginator = driver.find_element(By.XPATH, xpath_expression)
        except NoSuchElementException:
            break  # Break out of the loop if paginator element is not found
        paginator.click()
        time.sleep(5)
        logicielClass_element = driver.find_elements(By.XPATH, '//div[@class="mg_directory_text"]')
        for name_element in logicielClass_element:
            name = name_element.text.strip()
            studentLogiciel_names.append(name)
        print(len(studentLogiciel_names), "1")
        time.sleep(2)
        page_number += 1
    time.sleep(5)
    writeFilesForTrobiScopeEleveOnlyEveryone(studentLogiciel_names)


def scope_Teachers(driver):
    driver.get('https://myges.fr/student/home')

    wait = WebDriverWait(driver, 5)

    teachers = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="mg_menu_texte"]')))
    ActionChains(driver).move_to_element(teachers).click().perform()

    teachers_element = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Trombinoscope intervenants')]")))
    teachers_element.click()
    teachersList = []
    page_number = 0
    row = 1
    col = 1
    is_last_column = False
    teacher_id = 0
    while True:
        paginator_xpath = '//*[@id="teacherTrombiWidget:teacherDirectoryDataGrid_paginator_bottom"]/span[3]/span[' \
                          'count(preceding-sibling::span) >= ' + str(page_number) + ']'
        try:
            paginator = driver.find_element(By.XPATH, paginator_xpath)
        except NoSuchElementException:
            break  # Break out of the loop if paginator element is not found

        paginator.click()
        time.sleep(5)

        for i in range(row):
            teachersClass_element = driver.find_elements(By.XPATH, '//div[@class="mg_directory_text"]')
            if len(teachersClass_element) < 4:
                break

            for name_element in teachersClass_element:
                teacher_xpath = f'//*[@id="teacherTrombiWidget:teacherDirectoryDataGrid_content"]/table/tbody/tr[{row}]/td[{col}]/table/tbody/tr[2]/td'
                teacher = driver.find_element(By.XPATH, teacher_xpath)
                teacher_infos_xpath = f'//*[@id="teacherTrombiWidget:teacherDirectoryDataGrid:{teacher_id}:infosTeacher"]/span[2]'
                teacher_infos = driver.find_element(By.XPATH, teacher_infos_xpath)
                teacher_infos.click()
                teacher_plus_info = f'//*[@id="teacherTrombiWidget:teacherDirectoryDataGrid:{teacher_id}:chartPanel"]'
                teacher_infos = driver.find_element(By.XPATH, teacher_plus_info)
                info_teacher = teacher_infos.text.strip()
                teachersList.append(info_teacher)
                # teachersList.append(name)
                teacher_id += 1
                col += 1
                if col > 5:
                    col = 1
                    row += 1
                    is_last_column = True
            if is_last_column:
                break
        row = 1
        page_number += 1
        if is_last_column:
            is_last_column = False
    for teacher in teachersList:
        print(teacher)
    time.sleep(5)
    writeFilesForTeachers(teachersList)


def scrape_emploi(driver):
    driver.get('https://myges.fr/student/home')
    emploi_element = driver.find_element(By.XPATH, '//*[@id="mg_portal_nav"]/li[3]/a')
    emploi = emploi_element.click()
    planning = []
    column_data = []
    # table = driver.find_element(By.XPATH, '//table[@class="fc-agenda-days fc-border-separate"]')
    #
    # # Retrieve the header element representing the columns
    # header_element = table.find_element(By.XPATH, './/thead/tr')
    #
    # # Find the column elements
    # column_elements = header_element.find_elements(By.XPATH, './th[position() > 1]')
    #
    # # Iterate over the column elements to retrieve column values
    # for column_element in column_elements:
    #     column_name = column_element.text.strip()
    #
    #     # Find the column values
    #     column_index = column_element.get_attribute("class").split()[0].split('-')[-1]
    #     column_values = table.find_elements(By.XPATH, f'.//tbody/tr/td[{column_index}]/div')
    #
    #
    #     # Extract the column values
    #     column_values = [value.text.strip() for value in column_values]
    #
    #
    #
    #     # Print the column name and values
    #     print(f'{column_name}:')
    #     for value in column_values:
    #         print(value)
    #     print()
    week_parent_elements = driver.find_elements(By.XPATH,
                                                '//*[@id="calendar:myschedule_container"]/div/div/div/div/div/div/div')

    # Iterate over the week parent elements
    for index, week_parent_element in enumerate(week_parent_elements, start=1):
        # Update the XPath with the incremented index
        xpath = f'//*[@id="calendar:myschedule_container"]/div/div/div/div/div/div/div[{index}]'

        # Find all the child elements within the week parent element
        child_elements = week_parent_element.find_elements(By.XPATH, xpath)

        # Iterate over the child elements and retrieve their values
        for element in child_elements:
            value = element.text.strip()
            if value:
                planning.append(value)
                print(value)
    writeFilesPlaning(planning)



def writeFilesPlaning(fileType):
    filename = "exportFiles/Planing.txt"

    with open(filename, 'w') as file:
        for row in fileType:
            file.write(row + '\n')
def writeFilesForTrobiScopeEleveOnly3thClasses(fileType):
    filename = "exportFiles/trobiEleveOnly3thClasses.csv"
    translator = str.maketrans("", "", string.punctuation)

    with open(filename, 'w') as file:
        for row in fileType:
            file.write(row + '\n')


def writeFilesForTeachers(fileType):
    filename = "exportFiles/trobiTeachers.txt"
    translator = str.maketrans("", "", string.punctuation)

    with open(filename, 'w') as file:
        for row in fileType:
            file.write(row + '\n')


def writeFilesForTrobiScopeEleveOnlyEveryone(fileType):
    filename = "exportFiles/trobiEleveEveryone.txt"
    translator = str.maketrans("", "", string.punctuation)

    with open(filename, 'w') as file:
        for row in fileType:
            file.write(row + '\n')


def writeFilesForTrobiScopeEleveOnly3Al(fileType):
    filename = "exportFiles/trobiEleve3al.txt"
    # translator = str.maketrans("", "", string.punctuation)

    with open(filename, 'w') as file:
        for row in fileType:
            file.write(row + '\n')


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
    # scope_Teachers(driver)
    scrape_emploi(driver)
    scope_Trobinoscoupe_Etudiant(driver)
    driver.quit()

    uvicorn.run(app, host="0.0.0.0", port=8000)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
