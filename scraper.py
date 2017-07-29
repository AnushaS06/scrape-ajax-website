# Creating an lmxl object to use css selector
from lxml.etree import fromstring

# Request library
import requests

import json

class WholeFoodsScraper:

    API_url = 'http://www.wholefoodsmarket.com/views/ajax'
    scraped_stores = []

    def get_stores_info(self, page):
        # Entering the minimum required data for the API_url
        # Send back stores info
        data = {
        'view_name': 'store_locations_by_state',
        'view_display_id': 'state',
        'page': page
        }
        # Create Post Request
        response = requests.post(self.API_url, data=data)

        # Data required in second Element of the response
        # and as key 'data', this is the return objects
        # Given ChromeDevTool Preview of JSON
        return response.json()[1]['data']

    def parse_stores(self, data):
        # Create lxml Element Instance
        element = fromstring(data)

        for store in element.cssselect('.views-row'):
            store_info = {}
            # lxml etress css selector returns a list; thus always first time
            store_name = store.cssselect('.views-field-title a')[0].text
            street_address = store.cssselect('.street-block div')[0].text
            address_locality = store.cssselect('.locality')[0].text
            address_state = store.cssselect('.state')[0].text
            address_postal_code = store.cssselect('.postal-code')[0].text
            phone_number = store.cssselect('.views-field-field-phone-number div')[0].text

            try:
                opening_hours = store.cssselect('.views-field-field-store-hours div')[0].text
            except IndexError:
                # No opening hours means they are closed; thus not be Saved
                opening_hours = 'STORE CLOSED'
                continue

            full_address = "{},{},{} {}".format(street_address,
                                                address_locality,
                                                address_state,
                                                address_postal_code)
            # now we add info to a dictionary
            store_info = {
                        'name': store_name,
                        'full_address': full_address,
                        'phone': phone_number,
                        'hours': opening_hours
                        }
            # Saving the scraped data to stores list
            self.scraped_stores.append(store_info)

    def run(self):
        for page in range(2):
            # Retreive the data
            data = self.get_stores_info(page)
            # Parsing it
            self.parse_stores(data)
            print('scraped the page' + str(page))

        self.save_data()

    def save_data(self):
        with open('wholefoods_stores.json', 'w') as json_file:
            json.dump(self.scraped_stores, json_file, indent=4)

# To Run The file
if __name__=='__main__':
    scraper = WholeFoodsScraper()
    scraper.run()
