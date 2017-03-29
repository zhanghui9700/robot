#-*- coding=utf-8 -*-

import logging
import time

from django.conf import settings

from selenium import webdriver
from selenium.common import exceptions

LOG = logging.getLogger(__name__)


class SeleniumBrowser():

    def __init__(self):
        self.authenticated = False

    def __enter__(self):
        self.browser = webdriver.Firefox()
        self.browser.delete_all_cookies()
        return self

    def __exit__(self, type, value, traceback):
        try:
            time.sleep(settings.WAIT_INTERVAL)
            self.browser.quit()
        except Exception as ex:
            LOG.exception("selenium quit browser raise exception.")

    def _wait_element(self, func, selector):
        retries = 20
        while retries:
            try:
                LOG.info("_wait_element %s", selector)
                element = getattr(self.browser, func)(selector)
                if element.is_displayed():
                    return element
            except (exceptions.NoSuchElementException,
                    exceptions.StaleElementReferenceException):
                if retries <= 0:
                    raise
                else:
                    pass
            retries = retries - 1
            time.sleep(settings.WAIT_INTERVAL)
        raise exceptions.ElementNotVisibleException(
            "Element %s not visible despite waiting for %s seconds" % (
                selector, 20*settings.WAIT_INTERVAL)
            ) 

    def login(self):
        def _login(self):
            result = False
            try:
                self.browser.get(settings.PTX_LOGIN_URL)
                _user = self._wait_element("find_element_by_id", "username")
                _user = self.browser.find_element_by_id("username")
                _user.clear()
                _user.send_keys(settings.PTX_USER)
                LOG.info("login input username")

                _pwd = self.browser.find_element_by_id("password")
                _pwd.clear()
                _pwd.send_keys(settings.PTX_PASSWORD)
                LOG.info("login input password")

                login = self.browser.find_elements_by_xpath("//p[@class='ibm-button-link-alternate']/a")
                if len(login):
                    login = login[0]
                else:
                    login = self.browser.find_element_by_id("signinbutton")

                if not login:
                    raise Exception("selenium login page can't find login button") 

                login.click()

                LOG.info("login button click, waiting...")

                # change store
                for i in range(10):
                    time.sleep(settings.WAIT_INTERVAL)
                    LOG.info("wait login, current_url: %s", self.browser.current_url)
                    result = self.browser.current_url.find("WelcomeView") > -1
                    change_store = self.browser.current_url.find("ForceChangeStoreView") > -1

                    if result:
                        break
                    
                    if change_store:
                        _select = self._wait_element("find_element_by_id", "selectStore")
                        store = "US PC wholesale store"
                        for option in _select.find_elements_by_tag_name('option'):
                            if option.text == store:
                                option.click()
                                LOG.info("select store: %s",store)

                                _continue = self._wait_element("find_element_by_name", "Submit.x")
                                _continue.click()
                                
                                break
                        time.sleep(settings.WAIT_INTERVAL)
                        change_store_confirm = self.browser.current_url.find("ChangeStoreConfirmationView") > -1
                        if change_store_confirm:
                            self.browser.get(settings.PTX_WELCOME_URL)
                
                if not result:
                    for i in range(10):
                        time.sleep(settings.WAIT_INTERVAL)
                        LOG.info("after change sotre, current_url: %s", self.browser.current_url)
                        result = self.browser.current_url.find("WelcomeView") > -1
                        if result:
                            break
                        else:
                            pass 

                if result:
                    LOG.info("ptx login succeed")
                else:
                    LOG.error("ptx login failed, current_url: %s", self.browser.current_url)
            except Exception as ex:
                LOG.exception("ptx login raise exception.")

            return result

        if self.authenticated:
            return True;

        for i in range(1):
            try:
                if _login(self):
                    self.authenticated = True
                    break
            except:
                pass
        else:
            raise Exception("ptx login failed, break down")

    def _go_category(self, category):
        LOG.info("go to topcategory")
        self.browser.get(settings.TOP_CATEGORY_URL)

        time.sleep(settings.WAIT_INTERVAL)

        top_category = self.browser.find_element_by_xpath('//strong[contains(text(), "PC notebooks")]')
        top_category.click()

        top = top_category.find_element_by_xpath(".//ancestor::li")
        category_link= top.find_element_by_link_text(category)
        category_link.click()
        LOG.info("%s category link click", category)

    def _add_carts(self, product_ids=None):
        for i in range(20):
            time.sleep(settings.WAIT_INTERVAL*2)
            if self.browser.current_url.find("CategoryDisplay") > -1:
                break
        else:
            LOG.info("add_carts: %s", self.browser.current_url)
            raise Exception("add carts page not currect")

        LOG.info("category url: %s", self.browser.current_url)

        time.sleep(settings.WAIT_INTERVAL*2)

        line = self.browser.find_element_by_id("selectLines")
        for option in line.find_elements_by_tag_name('option'):
            if option.text == "100":
                option.click()
        go = self.browser.find_element_by_xpath('//input[@alt="Change lines per page"]')
        go.click()
    
        for i in range(20):
            time.sleep(settings.WAIT_INTERVAL*2)
            if self.browser.current_url.find("RetainUserSelectionCmd") > -1:
                break

        time.sleep(settings.WAIT_INTERVAL*2)

        max_page = 1
        jump_page = self.browser.find_element_by_id("jumpPage")
        for option in jump_page.find_elements_by_tag_name('option'):
            if int(option.text) > max_page:
                max_page = int(option.text)

        LOG.info("max page: %s", option.text)

        add_cart_succeed = False
        cart_counter = 0
        for index in xrange(max_page):
            jump = self.browser.find_element_by_xpath('//input[@alt="Jump to page"]')
            jump_page = self.browser.find_element_by_id("jumpPage")
            for option in jump_page.find_elements_by_tag_name('option'):
                if option.text == str(index+1):
                    option.click()
                    break
            jump.click()

            time.sleep(settings.WAIT_INTERVAL*5)
            LOG.info(self.browser.current_url)

            for p in product_ids:
                try:
                    product = self.browser.find_element_by_id(p)
                    product.click()
                    cart_counter += 1
                    add_cart_succeed = True
                    LOG.info("find product with id: %s, select it", p)
                except:
                    LOG.warning("can not find product with id: %s", p)

            if cart_counter == len(product_ids):
                break

        if not add_cart_succeed:
            raise Exception("can not find any product with category")

        add_to_cart = self._wait_element("find_element_by_name", "addToCartFlag.x")
        add_to_cart.click()

    def _view_cart(self):

        self._wait_element("find_element_by_id", "checkOut")

        checkout = self.browser.find_element_by_id("checkOut")
        checkout.click()
        
        continue_submit = self.browser.find_element_by_name("ibm-continue")
        # self.browser.save_screenshot("/path/to/file")
        continue_submit.click()

    def _input_logistic(self):
        def _input_value(self, ele_id, value):
            _input = self._wait_element("find_element_by_id",ele_id)
            _input.clear()
            _input.send_keys(value)
            LOG.info("input info: %s, value: %s", ele_id, value)

        def _select_by_text(self, ele_id, text):
            # try this:
            # from selenium.webdriver.support.ui import Select
            # select = Select(driver.find_element_by_id(element_id))
            # select.select_by_visible_text(label)
            _select = self._wait_element("find_element_by_id", ele_id)
            options = _select.find_elements_by_tag_name('option')
            LOG.error("select %s option count: %s", ele_id, len(options))
            for option in options:
                if option.text == text:
                    option.click()
                    LOG.info("input checkout select: %s, value: %s",
                                                        ele_id, text)
                    break
            else:
                LOG.error("input checkout select: %s, no option!", ele_id)

        input_fields = settings.CHECKOUT_INPUT_FIELDS
        select_fields = settings.CHECKOUT_SELECT_FIELDS 

        self._wait_element("find_element_by_id", "sp_email1")

        for element, value in input_fields:
            _input_value(self, element, value)

        for element, txt in select_fields:
            _select_by_text(self, element, txt)
            time.sleep(settings.WAIT_INTERVAL)
            _select_by_text(self, element, txt)

        time.sleep(settings.WAIT_INTERVAL)
        continue_submit = self.browser.find_element_by_name("OrderReviewCmd.x")
        #self.browser.save_screenshot("/tmp/checkout1-2.jpg")
        continue_submit.click()

    def _submit(self):
        continue_submit = self._wait_element("find_element_by_name", "OrderSubmitCmd.x")
        #self.browser.save_screenshot("/tmp/checkout2-2.jpg")
        continue_submit.click()
        time.sleep(settings.WAIT_INTERVAL)

    def auto_order(self, target=None):
        if not self.authenticated:
            self.login()

        if self.authenticated:
            for index, t in enumerate(target):
                self._go_category(category=t.get("category"))
                LOG.info("get category done [1/5]")

                self._add_carts(product_ids=t.get("product_ids"))
                LOG.info("add carts done [2/5]")
                
                self._view_cart()
                LOG.info("view cart done [3/5]")

                self._input_logistic()
                LOG.info("input checkout info done [4/5]")

                self._submit()
                LOG.info("submit order done [5/5]")
            LOG.info("auto order done")
        else:
            LOG.error("auto order failed, not authenticated!")
