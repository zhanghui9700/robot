#-*- coding=utf-8 -*-

import logging
import time

from django.conf import settings

from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.support.select import Select

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

    def _login(self):
        result = False
        try:
            self.browser.get(settings.PTX_LOGIN_URL)
            self._input_value("username", settings.PTX_USER)
            self._input_value("password", settings.PTX_PASSWORD)
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
                result = self.browser.current_url.find("WelcomeView") > -1
                change_store = self.browser.current_url.find("ForceChangeStoreView") > -1

                if result:
                    break
                else:
                    LOG.info("wait login, current_url: %s", self.browser.current_url)
                
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

            if result:
                LOG.info("ptx login succeed")
            else:
                LOG.error("ptx login failed, current_url: %s", self.browser.current_url)
        except Exception as ex:
            LOG.exception("ptx login raise exception.")

        return result

    def login(self):
        if self.authenticated:
            return True;

        for i in range(1):
            try:
                if self._login():
                    self.authenticated = True
                    break
            except:
                pass
        else:
            raise Exception("ptx login failed, break down")

    def _go_category(self, top, category):
        LOG.info("go to topcategory")
        self.browser.get(settings.TOP_CATEGORY_URL)

        top_category = self._wait_element("find_element_by_xpath", 
                            '//strong[contains(text(), "%s")]' % top)
        top_category.click()

        top = top_category.find_element_by_xpath(".//ancestor::li")
        category_link= top.find_element_by_link_text(category)
        category_link.click()
        LOG.info("%s category link click", category)

    def _add_carts(self, product_ids=None):
        for i in range(20):
            time.sleep(settings.WAIT_INTERVAL)
            if self.browser.current_url.find("CategoryDisplay") > -1:
                break
        else:
            LOG.info("add_carts: %s", self.browser.current_url)
            raise Exception("add carts page not currect")

        LOG.info("category url: %s", self.browser.current_url)

        LOG.info("adjust page size to 100")  
        line = Select(self._wait_element("find_element_by_id", "selectLines"))
        line.select_by_visible_text("100") 
        go = self.browser.find_element_by_xpath('//input[@alt="Change lines per page"]')
        go.click()
    
        for i in range(20):
            time.sleep(settings.WAIT_INTERVAL)
            if self.browser.current_url.find("RetainUserSelectionCmd") > -1:
                break

        max_page = 1
        jump_page = Select(self._wait_element("find_element_by_id", "jumpPage"))
        for option in jump_page.options:
            if int(option.text) > max_page:
                max_page = int(option.text)

        add_cart_succeed = False
        cart_counter = 0
        for index in xrange(max_page):
            LOG.info("max_page: %s, current: %s", max_page, index+1)
            if index > 0:
                jump_page = Select(self._wait_element("find_element_by_id", "jumpPage"))
                jump_page.select_by_visible_text(str(index+1))

                jump = self.browser.find_element_by_xpath('//input[@alt="Jump to page"]')
                jump.click()

            time.sleep(settings.WAIT_INTERVAL*3)

            for p in product_ids:
                try:
                    product = self.browser.find_element_by_id(p.number)
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

    def _click_cart_checkout(self):
        checkout = self._wait_element("find_element_by_id", "checkOut")
        checkout.click() 

    def _adjust_quantity(self, product_ids):
        # TODO
        import pdb; pdb.set_trace();
        carts = self.browser.find_elements_by_xpath("")

    def _view_cart(self, product_ids): 
        self._click_cart_checkout()  
        self._adjust_quantity(product_ids) 
        self._click_cart_checkout() 

        continue_submit = self.browser.find_element_by_name("ibm-continue")
        continue_submit.click()
        # make submit success
        pass

    def _input_value(self, ele_id, value):
        _input = self._wait_element("find_element_by_id", ele_id)
        _input.clear()
        _input.send_keys(value)
        LOG.info("input info: %s, value: %s", ele_id, value)

    def _select_by_text(self, ele_id, text):
        _select = Select(self._wait_element("find_element_by_id", ele_id))
        options = _select.options 
        LOG.info("select %s option count: %s", ele_id, len(options))
        if options:
            _select.select_by_visible_text(text)
            LOG.info("input checkout select: %s, value: %s",
                                                    ele_id, text)
        else:
            LOG.error("input checkout select: %s, no option!", ele_id)

        return _select.first_selected_option

    def _input_logistic(self): 
        input_fields = settings.CHECKOUT_INPUT_FIELDS
        select_fields = settings.CHECKOUT_SELECT_FIELDS 

        self._wait_element("find_element_by_id", "sp_email1")

        for element, value in input_fields:
            self._input_value(element, value)

        for element, txt in select_fields:
            for i in range(5):
                op = self._select_by_text(element, txt)
                if op and op.text == txt:
                    break

        time.sleep(settings.WAIT_INTERVAL)
        continue_submit = self.browser.find_element_by_name("OrderReviewCmd.x")
        continue_submit.click()

    def _submit(self):
        continue_submit = self._wait_element("find_element_by_name", "OrderSubmitCmd.x")
        #continue_submit.click()
        time.sleep(settings.WAIT_INTERVAL)

    def auto_order(self, target=None):
        if not self.authenticated:
            self.login()

        if self.authenticated:
            for index, t in enumerate(target):
                self._go_category(top=t.get("top"), category=t.get("category"))
                LOG.info("get category done [1/5]")

                try:
                    self._add_carts(product_ids=t.get("product_ids"))
                    LOG.info("add carts done [2/5]")
                except:
                    LOG.info("no carts break [2/5]")
                    continue
                
                self._view_cart(product_ids=t.get("product_ids"))
                LOG.info("view cart done [3/5]")

                self._input_logistic()
                LOG.info("input checkout info done [4/5]")

                self._submit()
                LOG.info("submit order done [5/5]")
            LOG.info("auto order done")
        else:
            LOG.error("auto order failed, not authenticated!")