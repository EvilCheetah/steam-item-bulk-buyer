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

import os
import re
import logging
import requests
from decimal import Decimal
from collections import defaultdict
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


USER_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'}
LOGIN_PAGE  = 'https://steamcommunity.com/login/'
DRIVER_PATH = 'chromedriver.exe'

LOGGER.setLevel(logging.WARNING)


class BulkBuyer:
	def __init__(self):
		"""
			Initializes the List to use it in following form:
				URL -> [Item Name, Number of Items]

			Boolean Variable is used for while loop when
			obtaining the items from the user.
		"""
		self._item_list   = defaultdict(dict)
		self._add_another = False
		self._total		  = 0.0

		self.main()

	def clear_screen(self):
		"""
			Clears the screen of the terminal based on the OS
		"""
		os.system('cls' if os.name == 'nt' else 'clear')

	def get_item_data(self, url):
		"""
			Returns the name of the Item based on URL
		"""
		soup       = BeautifulSoup(requests.get(url, headers = USER_HEADERS).content, 'html.parser')
		item_name  = soup.find('h2',  {'class': 'itemtitle'}).text
		item_price = float(re.sub(r'[^\d.]', '', soup.find('div', {'class': 'game_purchase_price price'}).text))
		return item_name, item_price

	def get_item(self):
		"""
			Gets the single item from the user
			and stores it in the _item_list
		"""
		self.clear_screen()
		print('Give URL of the item:')
		URL = str(input())
		print('How many do you want to buy?')
		amount = int(input())

		if URL not in self._item_list:
			name, price = self.get_item_data(URL)
			self._item_list[URL]['amount'] = amount
			self._item_list[URL]['name']   = name
			self._item_list[URL]['price']  = price

		else:
			self._item_list[URL]['amount'] += amount

		self.clear_screen()
		self.output_retrieved_items()
		print('Do you want to add another item? [Y/n]')
		choice = str(input())
		print()

		self._add_another = True if (choice == 'Y' or choice == 'y') else False

	def get_items_from_user(self):
		"""
			Gets the items from user
		"""
		self.get_item()
		while (self._add_another):
			self.get_item()

	def output_retrieved_items(self):
		"""
			Output the items that user wants to purchase
			from _item_list
		"""
		self.clear_screen()
		total = 0
		print('---------------Shopping List---------------\n')

		for data in self._item_list.values():
			print(f'Item Name:  {data["name"]}\n'
				  f'Amount:     {data["amount"]}\n'
				  f'Price/Item: {data["price"]:.2f}\n'
			)
			total += data['amount'] * data['price']

		print(f'Total: {total:.2f}\n'
			  '-------------------------------------------\n\n'
		)
		self._total = total

	def purchase_items(self):
		"""
			Purchases the items based on user input

			Loops over the URLS in the dict
			Clicks on the buttons only when they are clickable
			(using 'wait' method)
		"""
		with webdriver.Chrome(executable_path=DRIVER_PATH) as driver:

			driver.get(LOGIN_PAGE)

			self.clear_screen()
			input('Press ENTER to Perform the Purchase(-s)...')

			wait = WebDriverWait(driver, 10)

			for URL, data in self._item_list.items():

				print('\nCurrently processing:')
				print(data['name'])

				for _ in range(data['amount']):
					driver.get(URL)

					add_to_cart = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn_addtocart')))
					add_to_cart.click()

					confirmation = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn_green_steamui')))
					confirmation.click()

					purchase = wait.until(EC.element_to_be_clickable((By.ID, 'purchase_button_bottom_text')))
					purchase.click()

	def check_for_errors(self):
		"""
			Checks if the code has the errors or not specified data
		"""
		if ( DRIVER_PATH == '' ):
			raise Exception('You must specify the path to the Webdriver')

	def greeting_message(self):
		"""
			Output the Greeting message
		"""
		self.clear_screen()
		print('Welcome to Steam Bulk Buyer!\n\n'
			  'This script takes \'URL\' of the \'number of items\'\n'
			  'you would like to purchase\n\n'
			  'Press CTRL+C anytime to Terminate Program\n'
		)
		input('Press ENTER to Proceed...')

	def warning_message(self):
		"""
			After the user is done, warn them to check funds then login
		"""
		self.clear_screen()
		print(f'You need {self._total} to perform the operation\n')
		print('Before opening the browser:')
		print('Make sure you have ENOUGH funds for the purchase\n')
		print('Press ENTER to open the browser...')
		print('Login into your preffered account')
		input()

	def success_message(self):
		"""
			Outputs the 'SUCCESS' message when done
		"""
		self.clear_screen()
		print('Success!')
		print('Check your inventory!')

	def main(self):
		self.check_for_errors()
		self.greeting_message()
		self.get_items_from_user()
		self.output_retrieved_items()
		input('Press ENTER to Proceed...\n')
		self.warning_message()
		self.purchase_items()
		self.success_message()


if __name__ == '__main__':
	try:
		BulkBuyer()

	except KeyboardInterrupt:
		print('Interrupted')
