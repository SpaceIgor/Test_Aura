from selenium import webdriver
from selenium.webdriver.common.by import By


class BadOperationError(Exception):
    """"This exception is thrown when there is no specified operation"""
    pass


class TestParse(object):
        def __init__(self, driver, product: str, waiting_time: int):
            self.driver = driver
            self.product = product
            self.waiting_time = waiting_time

        def parse(self):
            self.test_shopping()

        def test_shopping(self):
            try:
                # Get URl for Amazon
                self.driver.get('https://www.amazon.com/')

                # Time of wait
                self.driver.implicitly_wait(self.waiting_time)

                # Searching product and clicking on button
                input_product = self.driver.find_element_by_id('twotabsearchtextbox')
                input_product.clear()
                input_product.send_keys(self.product)
                self.driver.find_element_by_id('nav-search-submit-button').click()
                self.driver.implicitly_wait(self.waiting_time)

                # Sorted
                self.driver.find_element_by_id('a-autoid-0-announce').click()
                self.driver.find_element_by_id('s-result-sort-select_3').click()
                self.driver.implicitly_wait(self.waiting_time)

                # Color matching and price fixing
                products = self.driver.find_elements(By.XPATH, '//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[2]/div/div/div/div/div/div[1]/div/div[2]/div/span/a')
                product_links = [link.get_attribute('href') for link in products]
                link_on_first_product_amazon = product_links[0]
                self.driver.get(link_on_first_product_amazon)
                self.driver.find_element_by_id('color_name_1').click()
                self.driver.implicitly_wait(self.waiting_time)

                price_product_amazon = self.driver.find_elements(By.XPATH, '//*[@id="corePrice_desktop"]/div/table/tbody/tr/td[2]/span[1]')
                price = [price.text[1:] for price in price_product_amazon]
                new_price_for_amazon = float(price[0])
                if len(price) != 0:
                    amazon_price = new_price_for_amazon
                else:
                    amazon_price = 0
                    print('Unfortunately, we can not find out the price of the product, as it is out of stock.')
                self.driver.implicitly_wait(self.waiting_time)

                # Get URl and country selection USA for Bestbuy
                self.driver.get('https://www.bestbuy.com/')
                self.driver.implicitly_wait(self.waiting_time)
                self.driver.get('https://www.bestbuy.com/?intl=nosplash')
                self.driver.implicitly_wait(self.waiting_time)

                # Searching product and clicking on button
                input_product_for_seaching = self.driver.find_element_by_id('gh-search-input')
                input_product_for_seaching.clear()
                input_product_for_seaching.send_keys(self.product)
                self.driver.find_element_by_class_name('header-search-button').click()
                self.driver.implicitly_wait(self.waiting_time)

                # Sorted
                self.driver.find_element_by_id('sort-by-select').click()
                self.driver.find_element_by_xpath('// *[ @ id = "sort-by-select"] / option[5]').click()
                self.driver.find_element_by_id('sort-by-select').click()
                self.driver.implicitly_wait(self.waiting_time)

                # Color matching and price fixing for bestbuy
                products_on_bestbuy = self.driver.find_elements_by_css_selector(".ratings-reviews [href]")
                links_on_first_product_bestbuy = [elem.get_attribute('href') for elem in products_on_bestbuy]
                link_on_first_product_bestbuy = links_on_first_product_bestbuy[0]
                self.driver.get(link_on_first_product_bestbuy)
                self.driver.implicitly_wait(self.waiting_time)

                price_product_bestbuy = self.driver.find_elements_by_class_name('sr-only')
                price_two = [price.text for price in price_product_bestbuy]
                get_price = price_two[0]
                new_price_for_bestbuy = get_price[29:]
                if len(price_two) != 0:
                    bestbuy_price = float(new_price_for_bestbuy)
                else:
                    bestbuy_price = 0
                    print('Unfortunately, we can not find out the price of the product, as it is out of stock.')

                self.driver.implicitly_wait(self.waiting_time)

                assert amazon_price > bestbuy_price

            except BadOperationError:
                print('Could not get the price of this product, or it is out of stock, please try again later')

            finally:
                self.driver.close()
                self.driver.quit()


def main():
    product = 'macbook air m1 16gb'
    waiting_time = 20

    driver = webdriver.Chrome()
    parser = TestParse(driver, product=product, waiting_time=waiting_time)
    parser.parse()


if __name__ == "__main__":
    main()