import re,requests
import json
import urllib2
from lxml import etree,html
from bs4 import BeautifulSoup
from pymongo import MongoClient

class angel_list_scrap:

    def __init__(self,s,main_url,headers):
        self.s = s 
        self.main_url = main_url
        self.headers = headers

    def get_login_page(self):
        login=s.get(main_url,headers=headers) #authenticity token is extracted from this page using the regex i mentioned below. This is required when you login to the page
        email = raw_input("Enter your email id : ")
        password = raw_input("Enter your AngelList Password : ")
        token=re.search("""<input name="authenticity_token" type="hidden" value="(.*?)"[^>]*?>""",login.text,re.S|re.I)
        print token.group(1)
        headers["Referer"]="https://angel.co/login"
        headers["Upgrade-Insecure-Requests"]="1"
        payload={"login_only":"true","user[email]":email,"user[password]":password,"authenticity_token":token.group(1),"utf8":"%25E2%259C%2593"}
        result=s.post("https://angel.co/users/login",headers=headers,data=payload,cookies=login.cookies)
        return result

    def get_json(self,json_url):
        startup_ids=[]
        json_id = self.s.get(json_url,headers=headers)
        soup = BeautifulSoup(json_id.text,"html.parser")
        startup_ids = soup.find('div',attrs={'class':'find g-module gray hidden shadow_no_border startup-container','data-startup_ids':True})
        print startup_ids['data-startup_ids']
        return startup_ids['data-startup_ids']
    
    def get_company_name(self,soup):
        name = soup.find('a',attrs={'class':'startup-link'})
        print name.text
        return name.text

    def get_company_link(self,soup):
        link = soup.find('a',attrs={'class':'website-link','href':True})
        print link['href']
        return link['href']
     
    def get_job_title(self,soup):
        job_title = []
        job_count = 0
        job_name = soup.find_all('div',attrs={'class':'title'})
        for job in job_name:
             job_title.insert(job_count,job.a.text)
             job_count = job_count+1
        return job_title

    def get_salary(self,soup):
        job_salary = []
        job_count = 0
        job_name = soup.find_all('div',attrs={'class':'compensation'})
        for job in job_name:
            job_salary.insert(job_count,job.text)
            job_count = job_count + 1
        return job_salary

    def get_experianced_in(self,soup):
        job_experiance = []
        job_count = 0
        job_name = soup.find_all('div',attrs={'class':'tags'})
        for job in job_name:
            job_experiance.insert(job_count,job.text)
            job_count = job_count + 1
        return job_experiance    
    
    def get_jobs(self,url,job_ids,db):
        job_titles = []
        job_salarys = []
        job_skills =[]
        job_timing = []
        job_location = []
        job_position = []
        new_job_ids = []
        skill_require = []
        job_count = 0
        new_job_ids = list(eval(job_ids))
        for each_id in new_job_ids:
                curl = url + str(each_id)
                print curl
                _id = each_id / 12 * 3 + 4
                isavail = db.job_database.find({"_id":_id}).count()>0
                if not isavail:
                    job_page = s.get(curl,headers=headers)
                    soup = BeautifulSoup(job_page.text,"html.parser")
                    company_name = self.get_company_name(soup)
                    company_link = self.get_company_link(soup)
                    job_titles = self.get_job_title(soup)        
                    job_salary = self.get_salary(soup)
                    job_skills = self.get_experianced_in(soup)
                    print job_skills
                    for job_skill in job_skills:
                        print  job_skill.encode('latin1')
                        jobsk = [li for li,js1 in enumerate(job_skill) if js1.encode('latin1')=="\xb7"]
                        print jobsk
                        job_timing.insert(job_count,job_skill[1:jobsk[0]])
                        job_location.insert(job_count,job_skill[jobsk[0]+1:jobsk[1]])
                        job_position.insert(job_count,job_skill[jobsk[1]+1:jobsk[2]])
                        skill_require.insert(job_count,job_skill[jobsk[2]+1:])
                        print job_timing
                        print job_location
                        print job_position
                        print skill_require
                        job_count = job_count + 1                                                
                    print company_name
                    print company_link
                    print job_titles
                    print job_salary
                    print job_timing
                    print job_location
                    print job_position
                    print skill_require
                    result = db.job_database.insert_one(
                        {
                            "_id" : _id,
                            "company_name" : company_name,
                            "company_link" : company_link,
                            "job_names" : job_titles,
                            "salary_for_job" : job_salary,
                            "job_timing " : job_timing,
                            "job_location" : job_location,
                            "job_position" : job_position,
                            "skills_needed" : skill_require
                            }
                        )
                    print "Inserted Successfully for company id "+str(each_id)
                    break
                else:
                    print "already available"
s=requests.session()
main_url="https://angel.co/login?utm_source=top_nav_home"
headers={"Content-Type":"application/x-www-form-urlencoded","Host":"angel.co","Origin":"https://angel.co"
,"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"} # Mostly you need to pass the headers . Default headers don't work always.  So be careful here
angel_list = angel_list_scrap(s,main_url,headers)
response = angel_list.get_login_page()
print response.url
current_url = "https://angel.co/jobs#find/f!%7B%22locations%22%3A%5B%221904-Bengaluru%2C%20KA%22%5D%7D"
job_id=angel_list.get_json(current_url)
print job_id
url = "https://angel.co/job_listings/browse_startups_table?startup_ids[]="
client = MongoClient()
db = client.jobcurator
angel_list.get_jobs(url,job_id,db)


