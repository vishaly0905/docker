#Program name    : download-copy.py                                                                        
#Purpose         : Download File through Web Scraping,Stored According to size and Create CSV 
#Author          : Vishal Yadav
#Create Date     : April 3 2022
#Last Update     : April 5 2022

import os
import csv
import time
import datetime
import os.path
import sys
import logging
from configparser import ConfigParser
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By

#creating log file

logging.basicConfig(filename='download.log',
                    filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')  
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.info("Log file started... ")
   
logger.info("Feching data from config file... ")
#creating config file object
config_object = ConfigParser()
config_object.read("config.ini")
#getting Data From Config File
download_info=config_object["download"]
url=download_info["url"]

chrome_driver_path=download_info["chrome_driver_path"]
logger.info(" Data Feched Successfully from config file... ")

#This Function will download file from given url
def download():
    logger.info("Download Started ")
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : "C:\\Users\Vishal_Yadav\down" }
    chromeOptions.add_experimental_option("prefs",prefs)

    try :
        driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chromeOptions)
        logger.warning("DeprecationWarning: executable_path has been deprecated, please pass in a Service object")
    except :
        logger.error(f"Unable to access chrome_driver_path or download path ")

    #with webdriver.Chrome(chrome_driver_path)as driver:
    try:    
        driver.get(url)
    except:
        logger.error("Unable to access url...Internet Connectivity")
        sys.exit(1)
    #search element by its class name
    try:
        a=driver.find_elements(By.CLASS_NAME , 'iconsminds-film')
    except:
        logger.error("Unable to access element by class_name...")
        sys.exit(1)
    for element in a :        
        element.click()
       
        print(element)
    logger.info(f"download complete ")
    time.sleep(5)
##Separate out the files into folders    
def separater(path,path1):
    logger.info(f"Separation Started ")
    #This will check existances of folder to store file.
    if not os.path.exists(path1):
                     os.makedirs(path1)
    logger.info(f"Folder Created to store Separeted folder ")
    #Fecthing path of file
    directory = os.fsencode(path)
    #loop throgh all file in the given directory
    for file in os.listdir(directory):
         filename = os.fsdecode(file)
         if filename.endswith(".txt") :
             #Getting size of file in bytes
             file_Size_bytes= os.path.getsize(f"{path}/{filename}")
             #coverting size of file into KB.
             file_Size_KBs=file_Size_bytes/1024
             #if size is greater then 100 kb then store in Below_100kb folder
             if file_Size_KBs < 100:
                 if not os.path.exists(f"{path1}/Below_100kb"):
                     os.makedirs(f"{path1}/Below_100kb")
                 try :    
                     Path(f"{path}/{filename}").rename(f"{path1}/Below_100kb/{filename}")
                 except :
                      logger.error(f"File already exists")
              #if size is in between 100 kb and 1MB then store in Bet_100_1000kb folder        
             if file_Size_KBs >= 100 and file_Size_KBs <= 1000:
                 if not os.path.exists(f"{path1}/Bet_100_1000kb"):
                     os.makedirs(f"{path1}/Bet_100_1000kb")
                 try:    
                     Path(f"{path}/{filename}").rename(f"{path1}/Bet_100_1000kb/{filename}")
                 except:
                     logger.error(f"File already exists")
            #if size is greater than 1MB then store in Above_1Mb folder           
             if not os.path.exists(f"{path1}/Above_1Mb"):
                     os.makedirs(f"{path1}/Above_1Mb")    
             if file_Size_KBs > 1000:
                 try:
                     Path(f"{path}/{filename}").rename(f"{path1}/Above_1Mb/{filename}")
                 except:
                     logger.error(f"File already exists")
             
             print(filename,file_Size_KBs," KB")
             
             continue
         else:
             continue
    print("Separation Successfull....")
    logger.info(f"File  store  in Separeted folder ") 
##For each file in respective folder create a csv file with 2 columns:

def Csv_Writer(path1) :
    logger.info(f"CSV creation started ")
    #storing folder in list
    folder_list = os.listdir(path1)
    for folder in folder_list :
        #extract the file from the folder
        file_list = os.listdir(f'{path1}/{folder}')
        for file in file_list:
            file1= file.strip('.txt')
            #create the csv file for particular file 
            csvfile = open(f'{path1}/{folder}/{file1}.csv', 'w+', newline='')
            #creating CSv writter object
            spamwriter = csv.writer(csvfile, delimiter=',')
            f= open (f'{path1}/{folder}/{file}') 
            count_vowels=0
            #Get list of all paragraph in file
            line_list=f.readlines()
            #iterate throgh all Paragraph
            for line in line_list:
                count_vowels=0
                line1=line.split(' ')
                #iterate throgh all word in paragraph
                for word in line1 :
                    word = word.lower()
                    vowel = ("a", "e", "i", "o", "u")
                    #iterate throgh all character in word till vowel enconter
                    
                    for char in word:
                        if char in vowel:
                            count_vowels=count_vowels+1
                            break
                        else:      
                            continue
                      
                spamwriter.writerow([ line , count_vowels , datetime.datetime.now()])
    print("CSV Created Successfully...")                
    logger.info(f"CSV creation successfull ")

                  


# Defining main function
def main():
    download()
    path=download_info["path"]   
    path1=input("Enter Path to Store Downloaded file According to size  :")
    separater(path,path1)
    Csv_Writer(path1)
    
# Using the special variable 
# __name__
if __name__=="__main__":
    main()

#C:/Users/Vishal_Yadav/Assignment1/






        

