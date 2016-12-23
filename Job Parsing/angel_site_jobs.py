import random
import re
import urllib2
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from pymongo import MongoClient

class AngelListScraping:

    def __init__(self,request,login_url,headers):
        self.request = request 
        self.login_url = login_url
        self.headers = headers

    def get_login_page(self):
        login_page=request.get(login_url,headers=headers) #authenticity token is extracted from this page using the regex i mentioned below. This is required when you login to the page
        email = raw_input("Enter your email id : ")
        password = raw_input("Enter your AngelList Password : ")
        token=re.search("""<input name="authenticity_token" type="hidden" value="(.*?)"[^>]*?>""",login_page.text,re.S|re.I)
        print token.group(1)
        headers["Referer"]="https://angel.co/login"
        headers["Upgrade-Insecure-Requests"]="1"
        login_details={"login_only":"true","user[email]":email,"user[password]":password,"authenticity_token":token.group(1),"utf8":"%25E2%259C%2593"}
        result=request.post("https://angel.co/users/login",headers=headers,data=login_details,cookies=login_page.cookies)
        return result

    def get_job_ids(self,job_id_url):
        startup_ids=[]
        job_id_page = self.request.get(job_id_url,headers=headers)
        soup = BeautifulSoup(job_id_page.text,"html.parser")
        job_ids = soup.find('div',attrs={'class':'find g-module gray hidden shadow_no_border startup-container','data-startup_ids':True})
        return job_ids['data-startup_ids']
    
    def get_company_name(self,soup):
        company_name = soup.find('a',attrs={'class':'startup-link'})
        return company_name.text

    def get_company_link(self,soup):
        try:
            company_link = soup.find('a',attrs={'class':'website-link','href':True})
            return company_link['href']
        except TypeError as e:
            return "-"

    def get_job_title(self,soup):
        job_title = []
        count = 0
        job_name = soup.find_all('div',attrs={'class':'title'})
        for job in job_name:
             job_title.insert(count,job.a.text)
             count = count+1
        return job_title

    def get_job_links(self,soup):
        links = []
        count = 0
        get_link = soup.find_all('div',attrs={'class':'title'})
        for link in get_link:
             links.insert(count,link.a['href'])
             count = count + 1
        print links
        return links

    def generate_id(self):
        _id = random.randrange(10000,1000000,20)
        return _id

    def is_id_available(self,_id,db):
        check = db.jobCollections.find({"_id":_id}).count()>0
        return check

    def is_inserted(self,job_link):
        check = db.jobCollections.find({"jobURL":job_link}).count()>0
        return check
        
    def  insert_db(self,company_name,company_link,job_titles,job_links,location,timing,skills,min_salary,max_salary,db):
        count = 0
        for job in  job_titles:
            _id = self.generate_id()
            while self.is_id_available(_id,db):
                _id = self.generate_id()
            skills[count] = skills[count].replace("\n","")
            if not skills[count] == "-":
                skills[count] = skills[count].split(", ");
            result = db.jobCollections.insert_one(
            {
                "_id" : _id,
                "companyName" : company_name,
                "companyLink" : company_link,
                "jobTitle" : job,
                "jobURL" : job_links[count],
                "jobLocation" : location[count],
                "jobTiming" : timing[count],
                "jobSkills" : skills[count],
                "minSalary" : min_salary[count],
                "maxSalary" : max_salary[count],
                "createdTime" : datetime.utcnow() 
                }
            )
            print "inserted"
            count = count + 1
            
    def get_job_page(self,job_link):
        job_page = request.get(job_link,headers=headers)
        return job_page

    def get_location(self,soup):
        location_tag = soup.find('div',attrs={'class':'high-concept'}).text
        location_tag = location_tag.encode('latin1')
        location = location_tag[0:location_tag.index('\xb7')-1]
        print location
        return location

    def get_timing(self,soup):
        timing_tag = soup.find('div',attrs={'class':'high-concept'}).text
        timing_tag = timing_tag.encode('latin1')
        timing = timing_tag[timing_tag.index('\xb7')+2:]
        print timing
        return timing

    def get_skill(self,soup):
        skill = '-'
        try:
            job_listing_metadata = soup.find('div',attrs={'class':'job-listing-metadata'})
            skill_name_tag = job_listing_metadata.find_all('div',attrs={'class':'s-vgBottom0_5'})
            skill_tag = job_listing_metadata.find_all('div',attrs={'class':'s-vgBottom2'})
            if skill_name_tag[0].text == 'Skills':
                skill = skill_tag[0].text
            print skill
            return skill
        except IndexError as e:
            return skill

    def get_salary_range(self,soup):
        salary_range = "-"
        count = 0
        job_listing_metadata = soup.find('div',attrs={'class':'job-listing-metadata'})
        salary_name_tag = job_listing_metadata.find_all('div',attrs={'class':'s-vgBottom0_5'})
        salary_tag = job_listing_metadata.find_all('div',attrs={'class':'s-vgBottom2'})
        for salary_name in salary_name_tag:
            if salary_name.text == 'Compensation':
                if "No Salary" not in salary_tag[count].text:
                    salary_range = salary_tag[count].text
            count = count + 1
        print salary_range
        return salary_range
        
                
    def get_company_details(self,job_listing_url,job_ids,db):
        job_titles = []
        job_links = []
        location = []
        timing = []
        min_salary = []
        max_salary = []
        min_max_list = []
        skills = []
        incr = 0
        for each_id in job_ids:
                job_listing_url = job_listing_url + str(each_id)
                print job_listing_url
                company_page = request.get(job_listing_url,headers=headers)
                company_soup = BeautifulSoup(company_page.text,"html.parser")
                company_name = self.get_company_name(company_soup)
                company_link = self.get_company_link(company_soup)
                job_titles = self.get_job_title(company_soup)        
                job_links = self.get_job_links(company_soup)
                while incr<len(job_titles):
                    print job_links[incr]
                    print self.is_inserted(job_links[incr])
                    if not self.is_inserted(job_links[incr]):
                        job_page = self.get_job_page(job_links[incr])
                        job_soup = BeautifulSoup(job_page.text,"html.parser")
                        location.insert(incr,self.get_location(job_soup))
                        timing.insert(incr,self.get_timing(job_soup))
                        skills.insert(incr,self.get_skill(job_soup))
                        salary_range = self.get_salary_range(job_soup)
                        min_max_list = map(int,re.findall('\d+',salary_range))
                        print min_max_list
                        if min_max_list:
                            minsalary = min_max_list[0]*1000
                            maxsalary = min_max_list[1]*1000
                            min_salary.insert(incr,minsalary)
                            max_salary.insert(incr,maxsalary)
                        else:
                            min_salary.insert(incr,"-")
                            max_salary.insert(incr,"-")
                        incr += 1
                    else:
                        print incr
                        job_links.pop(incr)
                        job_titles.pop(incr)
                        continue
                if job_links:
                    self.insert_db(company_name,company_link,job_titles,job_links,location,timing,skills,min_salary,max_salary,db)
                break
                    
request = requests.session()
login_url = "https://angel.co/login?utm_source=top_nav_home"
headers = {"Content-Type":"application/x-www-form-urlencoded","Host":"angel.co","Origin":"https://angel.co"
,"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"} # Mostly you need to pass the headers . Default headers don't work always.  So be careful here
scrap = AngelListScraping(request,login_url,headers)
login_response = scrap.get_login_page()
print login_response.url
job_search_url = "https://angel.co/jobs"
job_id = scrap.get_job_ids(job_search_url)
job_id =  list(eval(job_id))
job_listing_url = "https://angel.co/job_listings/browse_startups_table?startup_ids[]="
client = MongoClient()
db = client.jobCuratorDb
scrap.get_company_details(job_listing_url,job_id,db)


