from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import helpers


class UrbanRoutesPage:

    # Localizadores
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    button_round = (By.XPATH, '//button[@class="button round"]')

    comfort_plan = (
        By.XPATH,
        '//div[@class="tcard" and .//div[@class="tcard-title" and text()="Comfort"]]'
    )

    active_comfort = (
        By.XPATH,
        '//div[@class="tcard active" and .//div[@class="tcard-title" and text()="Comfort"]]'
    )

    phone_number_button = (By.CLASS_NAME, 'np-button')
    phone_number_field = (By.ID, 'phone')

    phone_code_field = (
        By.XPATH,
        '//input[@id="code" and @class="input"]'
    )

    next_button = (
        By.XPATH,
        '//button[@class="button full"]'
    )

    confirm_button = (
        By.XPATH,
        '//button[@class="button full" and text()="Confirmar"]'
    )

    payment_button = (By.CLASS_NAME, 'pp-button')

    add_card_button = (
        By.XPATH,
        '//div[@class="pp-title" and text()="Adicionar cartão"]'
    )

    card_number_field = (
        By.XPATH,
        '//input[@id="number"]'
    )

    card_code_field = (
        By.XPATH,
        '//input[@id="code" and @class="card-input"]'
    )

    card_link_button = (
        By.XPATH,
        '//button[@class="button full" and text()="Adicionar"]'
    )

    close_modal_button = (
        By.XPATH,
        '//button[@class="close-button section-close"]'
    )

    close_payment_modal = (
        By.XPATH,
        '//div[@class="section active"][.//div[@class="head" and normalize-space()="Método de pagamento"]]//button[@class="close-button section-close"]'
    )

    close_add_card_modal = (
        By.XPATH,
        '//div[@class="section active"][.//div[@class="pp-title" and normalize-space()="Adicionar cartão"]]//button[@class="close-button section-close"]'
    )

    comment_field = (By.ID, 'comment')

    blanket_switch = (
        By.XPATH,
        '//div[contains(text(),"Cobertor e lençóis")]//following-sibling::div//span[@class="slider round"]'
    )

    blanket_switch_status = (
        By.XPATH,
        '//div[contains(text(),"Cobertor e lençóis")]//following-sibling::div//input[@class="switch-input"]'
    )

    ice_cream_button = (
        By.XPATH,
        '//div[@class="r-counter-label" and contains(text(),"Sorvete")]'
        '//ancestor::div[@class="r-counter-container"]'
        '//div[@class="counter-plus"]'
    )

    ice_cream_count = (
        By.XPATH,
        '//div[@class="r-counter-label" and contains(text(),"Sorvete")]'
        '//ancestor::div[@class="r-counter-container"]'
        '//div[@class="counter-value"]'
    )

    order_button = (By.CLASS_NAME, 'smart-button')
    car_search_modal = (By.CLASS_NAME, 'order-header-title')

    def __init__(self, driver):
        self.driver = driver

    def wait_for_element(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def wait_for_clickable(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    # Definir endereço
    def set_from(self, address):
        self.wait_for_element(self.from_field).send_keys(address)

    def set_to(self, address):
        self.wait_for_element(self.to_field).send_keys(address)

    def get_from(self):
        return self.wait_for_element(self.from_field).get_attribute('value')

    def get_to(self):
        return self.wait_for_element(self.to_field).get_attribute('value')

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)
        self.wait_for_clickable(self.button_round).click()

    # Selecionar plano
    def select_comfort_plan(self):
        comfort = self.wait_for_element(self.comfort_plan)

        if 'active' not in comfort.get_attribute('class'):
            comfort.click()

    # Preencher telefone
    def fill_phone_number(self, phone_number, driver):
        self.wait_for_clickable(self.phone_number_button).click()
        self.wait_for_element(self.phone_number_field).send_keys(phone_number)
        self.wait_for_clickable(self.next_button).click()

        code = helpers.retrieve_phone_code(driver)

        self.wait_for_element(self.phone_code_field).send_keys(code)
        self.wait_for_clickable(self.confirm_button).click()

    # Adicionar cartão
    def fill_card(self, card_number, card_code):
        from selenium.webdriver.common.keys import Keys
        import time

        button = self.wait_for_element(self.payment_button)
        self.driver.execute_script("arguments[0].click();", button)

        time.sleep(1)

        add_card = self.wait_for_clickable(self.add_card_button)
        self.driver.execute_script("arguments[0].click();", add_card)

        time.sleep(1)

        card_field = self.wait_for_clickable(self.card_number_field)
        card_field.send_keys(card_number)

        code_field = self.wait_for_clickable(self.card_code_field)
        code_field.send_keys(card_code)

        # Remove o foco do campo CVV
        code_field.send_keys(Keys.TAB)

        time.sleep(1)

        add_button = self.wait_for_clickable(self.card_link_button)
        add_button.click()

        time.sleep(1)

        # Fecha a janela "Método de pagamento"
        close_payment = self.wait_for_clickable(self.close_payment_modal)
        self.driver.execute_script("arguments[0].click();", close_payment)

        time.sleep(1)

    # Comentário para o motorista
    def write_comment_for_driver(self, comment):
        self.wait_for_element(self.comment_field).send_keys(comment)

    # Cobertor e lenços
    def order_blanket_and_handkerchiefs(self):
        switch = self.wait_for_element(self.blanket_switch)
        self.driver.execute_script("arguments[0].click();", switch)

    def get_blanket_status(self):
        return self.wait_for_element(
            self.blanket_switch_status
        ).is_selected()

    # Sorvete
    def order_ice_cream(self, count):
        for i in range(count):
            self.wait_for_clickable(self.ice_cream_button).click()

    def get_ice_cream_count(self):
        return self.wait_for_element(self.ice_cream_count).text

    # Pedir táxi
    def order_taxi(self):
        self.wait_for_clickable(self.order_button).click()

    def get_car_search_modal(self):
        return self.wait_for_element(
            self.car_search_modal,
            timeout=15
        ).text