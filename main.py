import data
import helpers

from selenium import webdriver
from pages import UrbanRoutesPage


class TestUrbanRoutes:

    @classmethod
    def setup_class(cls):
        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Conectado ao servidor Urban Routes")
        else:
            print(
                "Não foi possível conectar ao Urban Routes. "
                "Verifique se o servidor está ligado e ainda em execução."
            )

        from selenium.webdriver import DesiredCapabilities

        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}

        cls.driver = webdriver.Chrome()
        cls.driver.get(data.URBAN_ROUTES_URL)

        cls.routes_page = UrbanRoutesPage(cls.driver)

    def test_set_route(self):
        self.routes_page.set_route(
            data.ADDRESS_FROM,
            data.ADDRESS_TO
        )

        assert self.routes_page.get_from() == data.ADDRESS_FROM
        assert self.routes_page.get_to() == data.ADDRESS_TO

    def test_select_plan(self):
        self.routes_page.select_comfort_plan()

    def test_fill_phone_number(self):
        self.routes_page.fill_phone_number(
            data.PHONE_NUMBER,
            self.driver
        )

    def test_fill_card(self):
        self.routes_page.fill_card(
            data.CARD_NUMBER,
            data.CARD_CODE
        )

    def test_comment_for_driver(self):
        self.routes_page.write_comment_for_driver(
            data.MESSAGE_FOR_DRIVER
        )

    def test_order_blanket_and_handkerchiefs(self):
        self.routes_page.order_blanket_and_handkerchiefs()

        assert self.routes_page.get_blanket_status() == True

    def test_order_2_ice_creams(self):
        self.routes_page.order_ice_cream(2)

        assert self.routes_page.get_ice_cream_count() == '2'

    def test_car_search_model_appears(self):
        self.routes_page.order_taxi()

        assert self.routes_page.get_car_search_modal() != ''

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()