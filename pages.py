from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import helpers


class UrbanRoutesPage:

    # Localizadores
    FROM_FIELD = (By.ID, 'from')
    TO_FIELD = (By.ID, 'to')
    BUTTON_ROUND = (By.XPATH, '//button[@class="button round"]')
    COMFORT_PLAN = (By.XPATH, '//div[contains(@class,"tcard") and .//div[@class="tcard-title" and text()="Comfort"]]')
    ACTIVE_COMFORT = (By.XPATH, '//div[@class="tcard active" and .//div[@class="tcard-title" and text()="Comfort"]]')
    PHONE_NUMBER_BUTTON = (By.CLASS_NAME, 'np-button')
    PHONE_NUMBER_FIELD = (By.ID, 'phone')
    PHONE_CODE_FIELD = (By.XPATH, '//input[@id="code" and @class="input"]')
    NEXT_BUTTON = (By.XPATH, '//button[@class="button full"]')
    CONFIRM_BUTTON = (By.XPATH, '//button[@class="button full" and text()="Confirmar"]')
    PAYMENT_BUTTON = (By.CLASS_NAME, 'pp-button')
    ADD_CARD_BUTTON = (By.XPATH, '//div[@class="pp-title" and text()="Adicionar cartão"]')
    CARD_NUMBER_FIELD = (By.XPATH, '//input[@id="number"]')
    CARD_CODE_FIELD = (By.XPATH, '//input[@id="code" and @class="card-input"]')
    CARD_LINK_BUTTON = (By.XPATH, '//button[@class="button full" and text()="Adicionar"]')
    CLOSE_MODAL_BUTTON = (By.XPATH, '//button[@class="close-button section-close"]')
    CLOSE_PAYMENT_MODAL = (By.XPATH, '//div[@class="section active"][.//div[@class="head" and normalize-space()="Método de pagamento"]]//button[@class="close-button section-close"]')
    CLOSE_ADD_CARD_MODAL = (By.XPATH, '//div[@class="section active"][.//div[@class="pp-title" and normalize-space()="Adicionar cartão"]]//button[@class="close-button section-close"]')
    COMMENT_FIELD = (By.ID, 'comment')
    BLANKET_SWITCH = (By.XPATH, '//div[contains(text(),"Cobertor e lençóis")]//following-sibling::div//span[@class="slider round"]')
    BLANKET_SWITCH_STATUS = (By.XPATH, '//div[contains(text(),"Cobertor e lençóis")]//following-sibling::div//input[@class="switch-input"]')
    ICE_CREAM_BUTTON = (By.XPATH, '//div[@class="r-counter-label" and contains(text(),"Sorvete")]//ancestor::div[@class="r-counter-container"]//div[@class="counter-plus"]')
    ICE_CREAM_COUNT = (By.XPATH, '//div[@class="r-counter-label" and contains(text(),"Sorvete")]//ancestor::div[@class="r-counter-container"]//div[@class="counter-value"]')
    ORDER_BUTTON = (By.CLASS_NAME, 'smart-button')
    CAR_SEARCH_MODAL = (By.CLASS_NAME, 'order-header-title')

    def __init__(self, driver):
        self.driver = driver

    def wait_for_element(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))

    def wait_for_clickable(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))

    # Definir endereço
    def set_from(self, address):
        self.wait_for_element(self.FROM_FIELD).send_keys(address)

    def set_to(self, address):
        self.wait_for_element(self.TO_FIELD).send_keys(address)

    def get_from(self):
        return self.wait_for_element(self.FROM_FIELD).get_attribute('value')

    def get_to(self):
        return self.wait_for_element(self.TO_FIELD).get_attribute('value')

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)
        self.wait_for_clickable(self.BUTTON_ROUND).click()

    # Selecionar plano
    def select_comfort_plan(self):
        comfort = self.wait_for_element(self.COMFORT_PLAN)

        if 'active' not in comfort.get_attribute('class'):
            comfort.click()

    def get_comfort_status(self):
        return self.wait_for_element(self.ACTIVE_COMFORT) is not None

    # Preencher telefone
    def fill_phone_number(self, phone_number, driver):
        self.wait_for_clickable(self.PHONE_NUMBER_BUTTON).click()
        self.wait_for_element(self.PHONE_NUMBER_FIELD).send_keys(phone_number)
        self.wait_for_clickable(self.NEXT_BUTTON).click()

        code = helpers.retrieve_phone_code(driver)

        self.wait_for_element(self.PHONE_CODE_FIELD).send_keys(code)
        self.wait_for_clickable(self.CONFIRM_BUTTON).click()

    def get_phone_number(self):
        return self.wait_for_element(self.PHONE_NUMBER_FIELD).get_attribute('value')

    # Adicionar cartão
    def fill_card(self, card_number, card_code):
        from selenium.webdriver.common.keys import Keys
        import time

        button = self.wait_for_element(self.PAYMENT_BUTTON)
        self.driver.execute_script("arguments[0].click();", button)

        time.sleep(1)

        add_card = self.wait_for_clickable(self.ADD_CARD_BUTTON)
        self.driver.execute_script("arguments[0].click();", add_card)

        time.sleep(1)

        card_field = self.wait_for_clickable(self.CARD_NUMBER_FIELD)
        card_field.send_keys(card_number)

        code_field = self.wait_for_clickable(self.CARD_CODE_FIELD)
        code_field.send_keys(card_code)

        # Remove o foco do campo CVV
        code_field.send_keys(Keys.TAB)

        time.sleep(1)

        add_button = self.wait_for_clickable(self.CARD_LINK_BUTTON)
        add_button.click()

        time.sleep(1)

        # Fecha a janela "Método de pagamento"
        close_payment = self.wait_for_clickable(self.CLOSE_PAYMENT_MODAL)
        self.driver.execute_script("arguments[0].click();", close_payment)

        time.sleep(1)

    def get_payment_method(self):
        return self.wait_for_element(self.PAYMENT_BUTTON).text

    # Comentário para o motorista
    def write_comment_for_driver(self, comment):
        from selenium.webdriver.common.keys import Keys

        field = self.wait_for_element(self.COMMENT_FIELD)
        field.send_keys(comment)
        field.send_keys(Keys.TAB)
    def get_comment(self):
        return self.wait_for_element(self.COMMENT_FIELD).get_attribute('value')

    # Cobertor e lenços
    def order_blanket_and_handkerchiefs(self):
        switch = self.wait_for_element(self.BLANKET_SWITCH)
        self.driver.execute_script("arguments[0].click();", switch)

    def get_blanket_status(self):
        return self.wait_for_element(self.BLANKET_SWITCH_STATUS).is_selected()

    # Sorvete
    def order_ice_cream(self, count):
        for i in range(count):
            button = self.wait_for_element(self.ICE_CREAM_BUTTON)
            self.driver.execute_script("arguments[0].scrollIntoView();", button)
            button.click()

    def get_ice_cream_count(self):
        return self.wait_for_element(self.ICE_CREAM_COUNT).text

    # Pedir táxi
    def order_taxi(self):
        self.wait_for_clickable(self.ORDER_BUTTON).click()

    def get_car_search_modal(self):
        return self.wait_for_element(self.CAR_SEARCH_MODAL, timeout=15).text