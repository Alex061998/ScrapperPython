# import webbrowser
#
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
#
#
# # def connection(username, password):
# #     options = webdriver.ChromeOptions()
# #     options.add_argument('--headless')
# #     options.add_argument('--no-sandbox')
# #     options.add_argument('--disable-dev-shm-usage')
# #     DRIVER_PATH = Service(r'D:\googleDriver\chromedriver.exe')
# #     driver = webdriver.Chrome(service=DRIVER_PATH, options=options)
# #     driver.get('https://www.myges.com/login')
# #
# #     wait = WebDriverWait(driver, 10)
# #
# #     username_input = WebDriverWait(driver, 10).until(
# #         EC.presence_of_element_located((By.ID, 'username')))
# #     password_input = WebDriverWait(driver, 10).until(
# #         EC.presence_of_element_located((By.ID, 'password')))
# #     submit_button = WebDriverWait(driver, 10).until(
# #         EC.presence_of_element_located((By.ID, 'input_submit')))
# #
# #     username_input.send_keys(username)
# #     password_input.send_keys(password)
# #     submit_button.click()
# #
# #     wait.until(EC.presence_of_element_located((By.ID, 'mg_container')))
# #
# #     return driver
#
#
# def connection(username, password):
#     DRIVER_PATH = Service(r'D:\googleDriver\chromedriver.exe')
#     driver = webdriver.Chrome(service=DRIVER_PATH)
#     driver.get('https://myges.fr/student/home')
#
    # wait = WebDriverWait(driver, 10)
    #
    # username_input = wait.until(EC.presence_of_element_located((By.ID, 'username')))
    # password_input = wait.until(EC.presence_of_element_located((By.ID, 'password')))
    # submit_button = wait.until(EC.presence_of_element_located((By.ID, 'input-submit')))
    #
    # username_input.send.keys(username)
    # password_input.send.keys(password)
    # submit_button.click()
#
#     # login_button = driver.find_element(By.XPATH, "//button[contains(next(), 'Se connecter')]")
#     # login_button.click()
#
#     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'mg_container')))
#
#     return driver
#
#
# def scrape_emploi(driver):
#     emploi_element = driver.find_element(By.ID, 'id_de_l_element_emploi_du_temps')
#     emploi = emploi_element.text
#
#     return emploi
#
#
# def scrape_notes(driver):
#     # Récupérer les notes
#     notes_element = driver.find_element(By.ID, 'id_de_l_element_notes')
#     notes = notes_element.text
#     return notes
#
#
# def scrape_trombinoscope(driver):
#     # Récupérer le trombinoscope
#     trombinoscope_element = driver.find_element(By.ID, 'id_de_l_element_trombinoscope')
#     trombinoscope = trombinoscope_element.text
#     return trombinoscope
