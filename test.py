from selenium import webdriver

browser = webdriver.Firefox()
browser.get("https://tieba.baidu.com/index.html")

new_list = browser.find_element_by_id('new_list')
user_name = browser.find_element_by_name ('user_name')
active = browser.find_element_by_class_name  ('active')
p = browser.find_element_by_tag_name ('p')