from selenium.webdriver.support.select import Select

from utils import Utils


class ProductForm:

    def __init__(self, driver):
        self.driver = driver

    def get_code_inputbox(self):
        return Utils.find_element_by_id_wait(self.driver, "StagedProduct_Code")

    def get_name_inputbox(self):
        return Utils.find_element_by_id_wait(self.driver, "StagedProduct_Caption")

    def get_current_code(self):
        return self.get_code_inputbox().get_attribute("value")

    def get_collection_select(self):
        return Select(Utils.find_element_by_id_wait(self.driver, "CollectionUnid"))

    def get_current_collection(self):
        return self.get_collection_select().first_selected_option.text

    def get_size_range_select(self):
        return Select(Utils.find_element_by_xpath_wait(self.driver, "//*[@class='size-templates-ddl']"))

    def get_current_size_range(self):
        return self.get_size_range_select().first_selected_option.text

    def get_price_inputbox(self):
        return Utils.find_element_by_xpath_wait(self.driver, "//input[contains(@id, 'CostPrice')]")

    def get_current_price(self):
        return float(self.get_price_inputbox().get_attribute("value"))

    def get_consumer_marketing_info_inputbox(self):
        return Utils.find_element_by_id_wait(self.driver, "StagedProduct_ConsumerMarketingInfo")

    def get_current_consumer_marketing_info(self):
        return self.get_consumer_marketing_info_inputbox().text

    def get_retailer_marketing_info_inputbox(self):
        return Utils.find_element_by_id_wait(self.driver, "StagedProduct_MarketingInfo")

    def get_current_retailer_marketing_info(self):
        return self.get_retailer_marketing_info_inputbox().text

    def get_save_button(self):
        return Utils.find_element_by_id_wait(self.driver, "SaveProduct")

    def get_leadtime_inputbox(self):
        return Utils.find_element_by_xpath_wait(self.driver, "//input[contains(@id, 'LeadTime')]")

    def get_rrp_inputbox(self):
        return Utils.find_element_by_xpath_wait(self.driver, "//input[contains(@id, 'Rrp')]")

    def get_startdate_inputbox(self):
        return Utils.find_element_by_xpath_wait(self.driver, "//input[contains(@id, 'StartDatepicker')]")

    def get_current_colours(self):
        colour_elements = self.driver.find_elements_by_xpath("//span[@class='pgtoListItem']")
        colours = []
        for element in colour_elements:
            colours.append(element.text)
        return colours

    def update_colours(self, colours):
        messages = []
        edit_colours_button = Utils.find_element_by_id_wait(self.driver, "EditColours")
        edit_colours_button.click()

        Utils.find_element_by_id_wait(self.driver, "DeselectAll").click()

        if type(colours) is str:
            new_colours = [x.strip() for x in colours.split(',')]
            colours = new_colours

        for colour in colours:
            try:
                colour_select = Select(Utils.find_element_by_id_wait(self.driver, "AvailableIds"))
                colour_select.deselect_all()
                colour_select.select_by_visible_text(colour)

                select_highlighted_button = Utils.find_element_by_id_wait(self.driver, "SelectHighlighted")
                select_highlighted_button.click()
            except:
                messages.append("Could not add colour {}".format(colour))

        update_close_button = Utils.find_element_by_id_wait(self.driver, "SaveDialog")
        update_close_button.click()
        return messages