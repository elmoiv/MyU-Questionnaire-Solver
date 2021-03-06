import time, random
from selenium import webdriver
from selenium.webdriver.support.ui import Select

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


import warnings
warnings.filterwarnings("ignore")

def Server():
    global driver
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    
    tmp_loc = options.binary_location
    try:
        options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        driver = webdriver.Chrome(chrome_options=options)
    except:
        options.binary_location = tmp_loc
        driver = webdriver.Chrome(chrome_options=options)

    driver.get('https://myu.mans.edu.eg/')

def wait_for_xpath(xpath, time):
    global driver
    WebDriverWait(driver, time).until(
            EC.presence_of_element_located(
            (By.XPATH, xpath)
            ))

def finish_questions(xpath, tab_number, questions_count):
    ## Choose random value for each question under tab
    for question_number in range(1, questions_count + 1):
        percentage = random.choice([20, 40, 60, 80, 100])
        xpath(f'//*[@id="{percentage}-{question_number}"]').click()
    
    # Proceed to save
    try:
        xpath('//*[@id="SaveQuestionnaire"]').click()
        xpath('//*[@id="popup_ok"]').click()
        ## Wait for next pop up
        wait_for_xpath('//*[@id="popup_ok"]', 20)
        xpath('//*[@id="popup_ok"]').click()
    except:
        print('>> Already Saved tab', tab_number)

def Core(name, password, semester, year):
    global driver

    xpath = driver.find_element_by_xpath
    
    # Log in
    print('>> Trying to log in...')
    xpath('//*[@id="frmLogin"]/div[1]/input').send_keys(name)
    xpath('//*[@id="frmLogin"]/div[2]/input').send_keys(password)
    xpath('//*[@id="frmLogin"]/div[4]/button').click()

    print('>>> Logged In Successfully')

    # Choose Questionnaire
    print('>> Navigating to Questionnaire...')
    xpath('/html/body/nav/div/div/div/div[1]/a/img').click()
    ## Click on the second question button (Visible for us)
    driver.find_elements_by_xpath('//*[contains(@class, "far fa-question-circle")]')[-1].click()

    # Switch to Questionnaire frame
    print('>> Searching for frame...')
    wait_for_xpath('//*[@id="div-data-container"]/iframe', 20)
    driver.switch_to_frame(xpath('//*[@id="div-data-container"]/iframe'))
    print('>>> Found frame.')

    print('>> Waiting for options to show...')
    wait_for_xpath('//*[@id="slcstuSemester"]', 20)
    print('>> Found options, Now selecting Year and Semester....')
    
    ## Choose Year
    xpath(f'//*[@id="slcstuAcademic"]/option[{year}]').click()

    ## Choose Semester
    xpath(f'//*[@id="slcstuSemester"]/option[{semester}]').click()
    
    ## Select Subjects option
    xpath('//*[@id="slcBasicCategory"]/option[2]').click()

    ## Wait for subject combobox to show and get number of subjects
    wait_for_xpath('//*[@id="slcstuCourses"]/option[1]', 20)
    subjects = Select(xpath('//*[@id="slcstuCourses"]'))
    print('>>> Found', len(subjects.options), 'Subjects.')

    ## Iterate through Subjects
    for subject_number in range(1, len(subjects.options) + 1):
        subject_choice = xpath(f'//*[@id="slcstuCourses"]/option[{subject_number}]')
        
        subject_choice.click()
        print('Subject', subject_number, ':', subject_choice.text)
       
        ## Switching between tabs
        for tab_number, questions_count in enumerate([3, 7, 3, 2], 1):
            wait_for_xpath(f'//*[@id="tabs"]/div[1]/button[{tab_number}]', 20)
            xpath(f'//*[@id="tabs"]/div[1]/button[{tab_number}]').click()

            ## If tab has stfff combo box
            if tab_number in [2, 3]:
                staff = Select(xpath('//*[@id="slcStaff"]'))
                
                ## Iterate through each staff
                for staff_number in range(1, len(staff.options) + 1):
                    xpath(f'//*[@id="slcStaff"]/option[{staff_number}]').click()
                    finish_questions(xpath, tab_number, questions_count)
            
            ## If tab is normal
            else:
                finish_questions(xpath, tab_number, questions_count)

    input('\n>> Done')


ID = input('> Enter your ID: ')
PASS = input('> Enter your Password: ')

# 1 : Current Year
# 2 : Last Year
YEAR = int(input('> Choose Year:\n[1] - Current Year\n[2] - Last Year\nYour choice: '))
if 1 > YEAR or YEAR > 2:
    input('Wrong Year, Dumbass -_-')
    exit(0)

# 1 : First Semester
# 2 : Second Semester
# 3 : Summer Semester
SEMESTER = int(input('> Choose Semester:\n[1] - First Semester\n[2] - Second Semester\n[3] - Summer Semester\nYour choice: '))
if 1 > SEMESTER or SEMESTER > 3:
    input('Wrong Semster, Dumbass -_-')
    exit(0)

Server()
Core(ID, PASS, SEMESTER, YEAR)
