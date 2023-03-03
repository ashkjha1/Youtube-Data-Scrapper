from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from flask_cors import CORS,cross_origin
import os
from flask import Flask, render_template, request
import time
import csv
# import pymongo
import logging

logging.basicConfig(filename="YTscrapper.log" , level=logging.INFO)

app = Flask(__name__)

@app.route("/")
@cross_origin()
def searchPage():
    return render_template("index.html")

# URL as per the given requirements
# url = "https://www.youtube.com/@PW-Foundation/videos"

@app.route("/search_result", methods = ["POST", "GET"])
@cross_origin()
def run_automation():
    if request.method == "POST":
        searchKey = request.form["searchkey"] # seachKey = @PW-Foundation
        url = "https://www.youtube.com/{searchKey}/videos"
        try:
            result_data = selenium_code(url)
            # return render_template('result.html', result_data=result_data)
            return result_data
        except:
            return "Something went Wrong"
    else:
        return render_template("index.html")

def selenium_code(url):
        try:
            csvResultList = [("title", "video_url", "video_thumbnail", "view_count", "timeofposting")]
            s = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=s)
            # driver = webdriver.Chrome()
            driver.maximize_window()
            driver.get(url)

            time_scroll = 3
            # scroll youtube web page
            while time_scroll > 0:
                driver.execute_script("window.scrollBy(0,500)")
                time_scroll -= 1
                time.sleep(3)

            try:
                # Code to scrape videos Hyperlink
                link_data = driver.find_elements(By.XPATH, '''//*[@id="thumbnail"]''')
                links = []
                for i in link_data:
                    links_static = i.get_attribute('href')
                    if links_static == None:
                        continue
                    else:
                        links.append(links_static)
            except:
                logging.info("Video_hyperlink")

            # for i in links[0:5]:
            #     print("Video Link",links.index(i),i)

            try:
                # Code to scrape thumbnails link
                img_data = driver.find_elements(By.XPATH, '''//*[@id="thumbnail"]/yt-image/img''')
                thumbnail = []
                for i in img_data:
                    thumbnail_static = i.get_attribute("src")
                    if thumbnail_static == None:
                        continue
                    else:
                        thumbnail.append(thumbnail_static) 
            except:
                logging.info("Thubnail_Link")

            # for i in thumbnail[0:5]:
            #     print("Thumbnail",thumbnail.index(i),i)

            try:
                # Code to scrape video title
                title_data = driver.find_elements(By.XPATH, '''//*[@id="video-title"]''')
                title = []
                for i in title_data:
                    title_static = i.text
                    if title_static == None:
                        continue
                    else:
                        title.append(title_static)
            except:
                logging.info("Video_title")

            # for i in title[0:5]:
            #     print("Title",title.index(i),i)

            try:
                # Code to scrape number of views
                view_data = driver.find_elements(By.XPATH, '''//*[@id="metadata-line"]/span[1]''')
                view_count = []
                for i in view_data:
                    view_static = i.text
                    if view_static == None:
                        continue
                    else:
                        view_count.append(view_static)
            except:
                logging.info("Number_Of_View")

            # for i in view_count[0:5]:
            #     print("View Count", view_count.index(i), i)       

            try:
                # Code to scrape time of posting
                time_data = driver.find_elements(By.XPATH, '''//*[@id="metadata-line"]/span[2]''')
                vid_time = []
                for i in time_data:
                    time_static = i.text
                    if time_static == None:
                        continue
                    else:
                        vid_time.append(time_static)
            except:
                logging.info("Time_Of_Posting")

            # for i in vid_time[0:5]:
            #     print("Time of Posting", vid_time.index(i), i)

            result = zip(title[0:5],links[0:5],thumbnail[0:5],view_count[0:5],vid_time[0:5])
            result_lst = list(result)

            # for i in result_lst:
            #     print(i)

            result_data = []
            for t,l,th,v,vt in result_lst:
                result_dict = {
                    "title": str(t),
                    "video_url": str(l),
                    "video_thumbnail": str(th),
                    "view_count": str(v),
                    "timeofposting": str(vt)
                }
                result_data.append(result_dict)
            # print(result_dict)
            logging.info("Log for final Result for web {}".format(result_dict))

            for i in result_lst:
                csvResultList.append(i)
            # print("csvResultList",csvResultList)
            logging.info("Log for final Result for CSV {}".format(csvResultList))

            with open("video_details.csv", 'w', encoding="utf-8") as f:
                    w = csv.writer(f)
                    for i in csvResultList:
                        w.writerow(i)
            
            return result_data

            driver.quit()

        except Exception as e:
            logging.info(e)
            return f"Something is wrong, Please check the URL again {e}"


    
if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 8000)