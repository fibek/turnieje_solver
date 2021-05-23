#!/usr/bin/env python3
import time
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import sys
import os
import pandas as pd

def writeFile(ans_map, taskfile):
    with open(taskfile, 'r+') as f:
        lines = f.readlines()
        for i in range(0, len(lines)):
            if lines[i].startswith("map<string,string> M;"):
                lines[i+1] = lines[i+1].strip()+ans_map+"\n"
                break
        f.seek(0)
        for line in lines:
            f.write(line)

def parse_table(table):
    data = table[0]
    dt = data["Unnamed: 5"].tolist()
    x = ""
    for s in dt:
        if type(s) is str:
            dataI = s[(s.find('Wczytano')+9):(s.find('oczekiwano')-2)]
            dataO = s[s.find('oczekiwano')+11:len(s)-1]
            x = x+"M["+dataI+"]="+dataO+";"
    return x

def send_task(driver, task):
    task.click()
    taskname = driver.find_element(By.NAME, "contest_submit[problem]").get_attribute('value')
    task_file_path = os.getcwd()+"/"+taskname+".cpp"
    time.sleep(1)
    driver.find_element(By.NAME, "contest_submit[solution_file]").send_keys(task_file_path)
    time.sleep(2)
    driver.find_element(By.ID, "submit_solution_button").click()
    time.sleep(15)
    data = pd.read_html(driver.find_element(By.XPATH, '//*[@id="report_table"]').get_attribute('outerHTML'))
    writeFile( parse_table(data), task_file_path)
    status = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[4]/div[2]/table[1]/tbody/tr/td[2]/dl/dd[1]/span").get_attribute('innerHTML')
    # driver.find_element(By.CSS_SELECTOR, "#report_modal > div:nth-child(3) > button:nth-child(1)").click()
    driver.refresh()
    return status


tournament_url = "https://turnieje.solve.edu.pl/contests/view/28"
# try: 
#     tournament_url = sys.argv[1];
# except:
#     print("Usage: ",sys.argv[0]," [link to tournament]")
#     exit()

driver = Firefox()
driver.get("https://turnieje.solve.edu.pl/users/login")

driver.find_element(By.NAME, "user_login[login]").send_keys("HelloFromHell");
driver.find_element(By.NAME, "user_login[password]").send_keys("06yg4iBFQ3kmt" + Keys.ENTER);

time.sleep(2)
driver.get(tournament_url)

time.sleep(2)
tasks = driver.find_elements(By.XPATH, "/html/body/div[2]/div/div[1]/div[2]/div[2]/div[1]/table/tbody/tr[*]/td[4]/a[2]")

num_of_tasks = len(tasks)
for i in range(1, num_of_tasks):
    xpath = "/html/body/div[2]/div/div[1]/div[2]/div[2]/div[1]/table/tbody/tr["+str(i)+"]/td[4]/a[2]"
    while True:
        task = driver.find_element(By.XPATH, xpath)
        status = send_task(driver,task)
        if status == "OK" or status == "Błąd kompilacji": break
        time.sleep(10)
    time.sleep(10)
