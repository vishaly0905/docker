# Program name    : download-copy.py
# Purpose         : Download File through Web Scraping,Stored According to size and Create CSV
# Author          : Vishal Yadav
# Create Date     : April 3 2022
# Last Update     : April 5 2022
import os
import csv
import time
import datetime
import os.path
import sys
import logging
import shutil
import pandas as pd
from configparser import ConfigParser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# This Function will download file from given url
# creating log file
logging.basicConfig(filename='Assignment_Basic.log',
                    filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.info("Log file started... ")
logger.info("Feching data from config file... ")
# creating config file object
config_object = ConfigParser()
config_object.read("config.ini")
# getting Data From Config File
download_info = config_object["download"]
url = download_info["url"]
chrome_driver_path = download_info["chrome_driver_path"]
logger.info(" Data Feched Successfully from config file... ")


def download():
    logger.info("Download Started ")
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"download.default_directory": "C:\\Users\Vishal_Yadav\down"}
    chromeOptions.add_experimental_option("prefs", prefs)
    try:
        driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chromeOptions)
    except:
        logger.error(f"Unable to access chrome_driver_path or download path ")
    # with webdriver.Chrome(chrome_driver_path)as driver:
    try:
        driver.get(url)
    except:
        logger.error("Unable to access url...Internet Connectivity")
        sys.exit(1)
    # search element by its class name
    try:
        a = driver.find_elements(By.CLASS_NAME, 'iconsminds-film')
    except:
        logger.error("Unable to access element by class_name...")
        sys.exit(1)
    for element in a:
        element.click()
        print(element)
    logger.info(f"download complete ")
    time.sleep(5)


##Separate out the files into folders
def separater(path, path1):
    logger.info(f"Separation Started ")
    # This will check existances of folder to store file.
    if not os.path.exists(path1):
        os.makedirs(path1)
    logger.info(f"Folder Created to store Separeted folder ")
    # Fecthing path of file
    directory = os.fsencode(path)
    # loop throgh all file in the given directory
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".txt"):
            # Getting size of file in bytes
            file_Size_bytes = os.path.getsize(f"{path}/{filename}")
            # coverting size of file into KB.
            file_Size_KBs = file_Size_bytes / 1024
            # if size is greater then 100 kb then store in Below_100kb folder
            if file_Size_KBs < 100:
                if not os.path.exists(f"{path1}/Below_100kb"):
                    os.makedirs(f"{path1}/Below_100kb")
                try:
                    shutil.move(f"{path}/{filename}", f"{path1}/Below_100kb/{filename}")
                    Csv_Writer(path1, "Below_100kb", filename)
                    df = pd.read_csv(f'{path1}/Below_100kb/' + filename.strip(".txt") + ".csv", header=0)
                    df.dropna().to_csv(f'{path1}/Below_100kb/Clean_' + filename.strip(".txt") + ".csv", header=False)
                    os.remove(f'{path1}/Below_100kb/' + filename.strip(".txt") + ".csv")
                except:
                    logger.error(f"File already exists")
            # if size is in between 100 kb and 1MB then store in Bet_100_1000kb folder
            if file_Size_KBs >= 100 and file_Size_KBs <= 1000:
                if not os.path.exists(f"{path1}/Bet_100_1000kb"):
                    os.makedirs(f"{path1}/Bet_100_1000kb")
                try:
                    shutil.move(f"{path}/{filename}", f"{path1}/Bet_100_1000kb/{filename}")
                    Csv_Writer(path1, "Bet_100_1000kb", filename)
                    df = pd.read_csv(f'{path1}/Bet_100_1000kb/' + filename.strip(".txt") + ".csv", header=0)
                    df.dropna().to_csv(f'{path1}/Bet_100_1000kb/Clean_' + filename.strip(".txt") + ".csv", header=False)
                    os.remove(f'{path1}/Bet_100_1000kb/' + filename.strip(".txt") + ".csv")
                except:
                    logger.error(f"File already exists")
            # if size is greater than 1MB then store in Above_1Mb folder
            if not os.path.exists(f"{path1}/Above_1Mb"):
                os.makedirs(f"{path1}/Above_1Mb")
            if file_Size_KBs > 1000:
                try:
                    shutil.move(f"{path}/{filename}", f"{path1}/Above_1Mb/{filename}")
                    Csv_Writer(path1, "Above_1Mb", filename)
                    df = pd.read_csv(f'{path1}/Above_1Mb/' + filename.strip(".txt") + ".csv", header=0)
                    df.dropna().to_csv(f'{path1}/Above_1Mb/Clean_' + filename.strip(".txt") + ".csv", header=False)
                    os.remove(f'{path1}/Above_1Mb/' + filename.strip(".txt") + ".csv")
                except:
                    logger.error(f"File already exists")
            print(filename, file_Size_KBs, " KB")
            continue
        else:
            continue
    print("Separation Successfull....")
    logger.info(f"File  store  in Separeted folder ")


##For each file in respective folder create a csv file with 2 columns:
def Csv_Writer(path1, folder, file):
    file1 = file.strip('.txt')
    # create the csv file for particular file
    csvfile = open(f'{path1}/{folder}/{file1}.csv', 'w')
    # creating CSv writter object
    spamwriter = csv.writer(csvfile, delimiter=',')
    spamwriter.writerow(["Paragraph", "count_vowels", "Time"])
    f = open(f'{path1}/{folder}/{file}')
    count_vowels = 0
    # Get list of all paragraph in file
    line_list = f.readlines()
    # iterate throgh all Paragraph
    for n in range(0, len(line_list)):
        if n != 0 and n % 2 != 0:
            continue
        line = line_list[n]
        count_vowels = 0
        line1 = line.split(' ')
        # iterate throgh all word in paragraph
        for word in line1:
            word = word.lower()
            vowel = ("a", "e", "i", "o", "u")
            # iterate throgh all character in word till vowel enconter
            for char in word:
                if char in vowel:
                    count_vowels = count_vowels + 1
                    break
                else:
                    continue
        spamwriter.writerow([line, count_vowels, datetime.datetime.now()])
    # print("CSV Created Successfully...")
    logger.info(f"CSV creation successfull ")


# Defining main function
def main():
    # Function Call
    download()
    path = download_info["path"]
    path1 = input("Enter Path to Store Downloaded file According to size  :")
    separater(path, path1)
    # csv_cleaner(path1)


# Using the special variable
if __name__ == "__main__":
    main()
