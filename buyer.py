'''
	Author: Eugene Moshchyn
	
	Python Version: Python 3.7+
	
	Purpose:
		- If you are buying items from the Steam Store in bulk,
		  you could notice that some items are stored in single cell
		  as single item with "amount" number below the thumbnail
		  of the item(such as in Rust).
		  
		  This program performes the individual purchases of the provided
		  items, putting all the items as individual items, occupying multiple
		  spaces in inventory.
	
	Requirements:
		- Chrome browser itself
		- Chrome webdriver that can be downloaded:
				https://sites.google.com/a/chromium.org/chromedriver/downloads
'''

LOGIN_PAGE  = "https://steamcommunity.com/login/"


from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from time import sleep
from DRIVER_PATH import DRIVER_PATH

class itemBuyer:
	def __init__(self):
		self._itemList  = {}
		self.addAnother = False
		
		self.main()

	def obtainListFromUser(self):
		self.getItem()
		while (self.addAnother):
			self.getItem()
	
	def outputTheList(self):
		print("\n\n------------To Be Bought------------\n")
		for URL, amount in self._itemList.items():
			print("URL:     ", URL)
			print("Amount:  ", amount)
			print()
		print("------------------------------------\n\n")
			
	def warnUser(self):
		print("Login into your account")
		print("Make sure you have enough funds to perform the operation\n")
		print("Press ENTER to proceed...")
		input()
		print("\nWhen you are done Loggin in...")
		print("Press ENTER...")
	
	def performOperation(self):
		with webdriver.Chrome(executable_path=DRIVER_PATH) as driver:
			
			driver.get(LOGIN_PAGE)
			input() 
			
			for URL, amount in self._itemList.items():
				
				print("\nCurrently processing:")
				print(URL)
				
				for i in range(amount):
					actions  = ActionChains(driver)
					driver.get(URL)
					
					sleep(2)
					
					next = driver.find_element(By.CLASS_NAME, "btn_addtocart")
					actions.move_to_element(next).perform()
					actions.click().perform()
					
					sleep(2)
					
					actions  = ActionChains(driver)
					next = driver.find_element(By.XPATH, "/html/body/div[3]/div[3]/div/div[2]/div[1]")
					actions.move_to_element(next).perform()
					actions.click().perform()
					
					sleep(2)
					
					actions  = ActionChains(driver)
					next = driver.find_element(By.ID, "purchase_button_bottom_text")
					actions.move_to_element(next).perform()
					actions.click().perform()
					
					sleep(1)

	def getItem(self):
		print("Give URL of the item:")
		URL = str(input())
		print("How many do you want to buy?")
		Amount = int(input())
		
		if URL not in self._itemList:
			self._itemList[URL] = Amount
		
		else:
			self._itemList[URL] += Amount
		
		print()
		print("Do you want to add another item? [Y/n]")
		choice = str(input())
		print()
		
		self.addAnother = True if (choice == 'Y' or choice == 'y') else False
	
	def Done(self):
		print("Success!")
		print("Check your inventory!")
	
	def main(self):

		self.obtainListFromUser()
		self.outputTheList()
		self.warnUser()
		self.performOperation()
		self.Done()


if __name__ == "__main__":
	try:
		itemBuyer()
		
	except KeyboardInterrupt:
		print("Interrupted")
