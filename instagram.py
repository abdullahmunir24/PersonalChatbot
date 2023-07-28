from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def login_instagram(username, password):
    say("Logging into your Instagram account, sir...")

    # Initialize the WebDriver (Safari)
    driver = webdriver.Safari()
    # Open Instagram login page
    driver.get('https://www.instagram.com/accounts/login/')

    # Wait for the page to load
    time.sleep(10)

    # Find the username and password input fields using CSS selector
    username_input = driver.find_element(By.XPATH, "//input[@name='username']")
    password_input = driver.find_element(By.XPATH, "//input[@name='password']")

    username_input.send_keys(username)
    password_input.send_keys(password)

    # Press Enter to submit the form
    login_button = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]')
    login_button.click()

    time.sleep(5)
