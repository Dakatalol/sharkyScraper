from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent



def browser_source():
    url = 'https://sharky.fi/lend'
    user_agent = UserAgent().random
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    # options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
    driver.get(url)
    driver.execute_script('return document.readyState;')
    wait_element = "/html//div[@id='__next']//main/div[2]/div[4]/div[4]/div[1]/span[@class='font-pingfang']"
    WebDriverWait(driver, 20).until(ec.presence_of_element_located((By.XPATH, wait_element)))
    browser_source = driver.page_source
    driver.close()
    return browser_source
