import time
import pandas as pd

from selenium import webdriver
import chromedriver_binary

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# =========================================================
# ACCOUNT
# =========================================================

USERNAME = "vutuanhai237@gmail.com"
PASSWORD = "Concho123@"


# =========================================================
# LOGIN
# =========================================================

def login_hackerrank(driver):

    login_url = "https://www.hackerrank.com/auth/login"

    driver.get(login_url)

    time.sleep(3)

    # email input
    email_box = driver.find_element(
        By.XPATH,
        '//input[@type="text" or @name="username"]'
    )

    # password input
    password_box = driver.find_element(
        By.XPATH,
        '//input[@type="password"]'
    )

    email_box.clear()
    email_box.send_keys(USERNAME)

    password_box.clear()
    password_box.send_keys(PASSWORD)

    time.sleep(1)

    # submit login
    password_box.send_keys(Keys.RETURN)

    print("LOGIN SUBMITTED")

    # wait login
    time.sleep(8)

    print("CURRENT URL:", driver.current_url)


# =========================================================
# EXCEL
# =========================================================

def read_score_sheet(class_name, sub_class):

    sheet = pd.read_excel(
        '../' + class_name + '/' + sub_class + '.xlsx'
    )

    return sheet


# =========================================================
# CRAWLER
# =========================================================

def crawl_score(
    class_name,
    join_class,
    sub_class,
    lab,
    contest_name
):

    df = read_score_sheet(class_name, sub_class)

    # =========================================
    # CREATE DRIVER ONLY ONCE
    # =========================================

    driver = webdriver.Chrome()

    # =========================================
    # LOGIN FIRST
    # =========================================

    login_hackerrank(driver)

    # =========================================
    # CRAWL
    # =========================================

    for i in range(1, 100):

        url = (
            'https://www.hackerrank.com/contests/'
            + contest_name
            + '/leaderboard/'
            + str(i)
        )

        print("\n================================")
        print(url)

        driver.get(url)

        time.sleep(5)

        try:

            table = driver.find_element(
                by=By.XPATH,
                value='//*[@id="leaders"]'
            )

            data = [
                item.text
                for item in table.find_elements(
                    by=By.XPATH,
                    value='//*[@class="leaderboard-list-view"]'
                )
            ]

        except Exception as e:

            print("TABLE ERROR:", e)

            break

        print("ROWS:", len(data))

        if len(data) == 0:

            print("NO MORE DATA")

            break

        for item in data:

            try:

                item_collection = item.splitlines()

                print(item_collection)

                # username line
                student_id = (
                    item_collection[1]
                )[-8:]

                if student_id.isdigit():

                    student_id = int(student_id)

                    score = float(item_collection[2])

                    submit_time = item_collection[3]

                    index = (
                        df.index[
                            df['ID'] == student_id
                        ].tolist()
                    )

                    print(
                        f"ID={student_id} "
                        f"SCORE={score}"
                    )

                    df.loc[index, lab] = score

            except Exception as e:

                print("ROW ERROR:", e)

        time.sleep(1)

    # =========================================
    # SAVE
    # =========================================

    driver.quit()

    df.to_excel(
        '../' + class_name + '/' + sub_class + '.xlsx',
        index=False
    )

    print("SAVED")


# =========================================================
# MAIN
# =========================================================

class_name = 'it002q216'

for class_name in ['it002q216']:

    for join_class in [1, 2]:

        for lab in [1, 2, 3, 4, 5]:

            sub_class = class_name + str(join_class)

            contest_name = (
                f'bai-tap-thuc-hanh-lab-{lab}-'
                f'{class_name[:5]}-'
                f'{class_name[5:]}-'
                f'{join_class}'
            )

            print("\n################################")
            print(contest_name)

            crawl_score(
                class_name,
                join_class,
                sub_class,
                lab,
                contest_name
            )