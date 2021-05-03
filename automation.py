from selenium.webdriver.common.by import By
from selenium.common import exceptions 
from selenium.webdriver.common.keys import Keys
import logging
import random
import time

post_comment_for_unrecommend = "We are extremely disappointed to hear that you feel your experience with us has been difficult. We can assure you we as a community and staff pride ourselves on customer service to deliver a high level community experience. Please come in to speak with our manager today. We always encourage healthy dialogue to help find a resolution that will benefit all parties and we want to help you immediately."
post_comment_for_recommend = "Thank you so very much for the kind and thoughtful review of our property. We take a tremendous sense of pride to deliver the customer experience you have grown to expect. Our staff is always here for you! We also know you have a choice where you call, home, and we are grateful it is with us."


class FacebookAutomation:

	def __init__(self,driver,urls,user_fb_name,user_email,password):
		self.driver = driver
		self.gen_urls = (url for url in urls)
		self.user_fb_name = user_fb_name
		self.user_email = user_email
		self.password = password

	def login(self):
		#Entering Email and Password
		username_box = self.driver.find_element_by_id('email') 
		username_box.send_keys(self.user_email) 	  
		password_box = self.driver.find_element_by_id('pass') 
		password_box.send_keys(self.password) 

		#Pressing The Login Button  
		login_box = self.driver.find_element(By.XPATH, '//button[text()="Log In"]')
		time.sleep(2)
		login_box.click() 

	def logout(self):
		profile_block = self.driver.find_element(By.XPATH, '//div[@role="button"][@aria-label="Account"]')
		#click profile icon
		profile_block.click()
		time.sleep(5)
		#search logout container
		logout_flyout_container = self.driver.find_element(By.XPATH, '//div[@data-nocookies="true"]')
		logout_button = logout_flyout_container.find_element(By.XPATH, './/div[@role="button"]')
		#click logout button
		logout_button.click()
		time.sleep(5)
		return True

	def openReviewPage(self):
		try:
			#open business page and return list of dom elements recommended / unrecommended users
			open_url = next(self.gen_urls)
			logging.info('open {}'.format(open_url))
			self.driver.get(open_url) 
			time.sleep(10)
			#scroll down in page 1
			self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight || document.documentElement.scrollHeight);')
			time.sleep(5)
			#scroll top 
			self.driver.execute_script('window.scrollTo(0,0);')
			#get review blocks
			review_articles = (y for y in self.driver.find_elements(By.XPATH, '//div[@role="article"][@aria-describedby]'))
			self.readReviewArticles(next(review_articles), review_articles)
			time.sleep(5)
			logging.info('done {}'.format(open_url))
			#review next url
			self.openReviewPage()
		except StopIteration:
			return False
		

	def readReviewArticles(self,review_article,review_articles):
		try:
			check_if_already_posted_comment = review_article.find_element_by_xpath(".//div[contains(.,'{}')][@role='article']".format(self.user_fb_name))
			#comment alreay posted moving to next review
			self.readReviewArticles(next(review_articles), review_articles)
		except exceptions.NoSuchElementException,e:
			logging.info('no prior comment detected posting comment!')
			try:  
				#negative test to check if does not recommend
				does_not_recommend_element = self.readTypeOfReview(review_article)
				if does_not_recommend_element:
					self.negativeComment(review_article)
				else:
					self.positiveComment(review_article)
				#wait for few sec for human behavior and again check for negative test
				time.sleep(5)
				self.readReviewArticles(next(review_articles), review_articles)
			except exceptions.StaleElementReferenceException,e:
				return False
			except StopIteration:
				return False
		except StopIteration:
			return False

		

	def readTypeOfReview(self,element_source):
		# return type of element recommended / unrecommended
		try:  
			doesNotRecommend = element_source.find_element_by_xpath(".//h2[contains(., 't recommend')]")
			return doesNotRecommend
		except exceptions.NoSuchElementException,e:
			return False
		except exceptions.StaleElementReferenceException,e:
			logging.info(e)
		
	def negativeComment(self,review_article):
		try:  
			input_container = review_article.find_element_by_xpath(".//div[@aria-label='Write a comment']")
			input_container.send_keys(post_comment_for_unrecommend)
			input_container.send_keys(Keys.ENTER)
			time.sleep(5)
		except exceptions.NoSuchElementException,e:
			logging.info(e)

	def positiveComment(self,review_article):
		try:  
			input_container = review_article.find_element_by_xpath(".//div[@aria-label='Write a comment']")
			input_container.send_keys(post_comment_for_recommend)
			input_container.send_keys(Keys.ENTER)
			time.sleep(5)
		except exceptions.NoSuchElementException,e:
			logging.info(e)
			
		



