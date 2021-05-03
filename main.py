from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from automation import FacebookAutomation
import os
import time
import json

# instantiate a chrome options object so you can set the size and headless preference
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("window-size=1200x600")

print(os.getcwd())
# place chromedriver in above path
chrome_driver = os.getcwd() +"/chromedriver"
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)

#read listing data from api, for every user create new object of type FacebookAutomation 
def Analyzer(listing,gen_listings):
	try:
		#Opening Facebook.
		driver.get('https://www.facebook.com/')
		time.sleep(5) 

		fb_automate = FacebookAutomation(driver,listing['review_pages'],listing['user_fb_name'],\
			listing['user_email'],listing['password'])
		#login in user account
		fb_automate.login()
		time.sleep(5)
		#open review page and post comment
		fb_automate.openReviewPage()
		time.sleep(5)
		fb_automate.logout()
		# start analyzing next listing from lisiting generator
		Analyzer(next(gen_listings),gen_listings)
	except StopIteration:
		print('all listings analyzed or listings array empty')
		driver.quit() 

if __name__ == "__main__":
	try:
		with open(os.getcwd() +"/listing.json") as f:
			data = json.load(f)
			gen_listings = (listing for listing in data['listings'])
			Analyzer(next(gen_listings),gen_listings)
	except ValueError:
		print('No JSON object could be decoded')
		driver.quit()
	except StopIteration:
		print('listings array empty')
		driver.quit() 
	
		


