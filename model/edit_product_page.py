from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from StatusObject import StatusObject
from model.locators import ProductForm
from model.object.base_page_element import BasePageElement, Inputbox, Selector, Button
from model.object.base_page_object import BasePageObject
from utils import Utils


class CodeInputbox(Inputbox):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=ProductForm.code_inputbox
        )


class NameInputbox(Inputbox):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=ProductForm.name_inputbox
        )


class CollectionSelect(Selector):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=ProductForm.collection_select
        )


class ImageUploader(Inputbox):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=ProductForm.image_uploader
        )


class SizeRangeSelect(Selector):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=ProductForm.size_range_select
        )


class PriceInputbox(Inputbox):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=ProductForm.price_inputbox
        )


class ConsumerMarketingInfoInputbox(Inputbox):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=ProductForm.consumer_marketing_info_inputbox
        )


class RetailerMarketingInfoInputbox(Inputbox):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=ProductForm.retailer_marketing_info_inputbox
        )


class SaveButton(Button):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=ProductForm.save_button
        )


class LeadTimeInputbox(Inputbox):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=ProductForm.leadtime_inputbox
        )


class RrpInputbox(Inputbox):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=ProductForm.rrp_inputbox
        )


class StartDateInputbox(Inputbox):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=ProductForm.start_date_inputbox
        )


class ExpandAllOptionsButton(Button):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=ProductForm.expand_all_button
        )


class SpecialLengthOptionButton(Button):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=ProductForm.special_length_option
        )


class EditProductPage(BasePageObject):
    def __init__(self, driver):
        self.driver = driver
        self.code_inputbox = CodeInputbox(driver)
        self.name_inputbox = NameInputbox(driver)
        self.collection_select = CollectionSelect(driver)
        self.image_uploader = ImageUploader(driver)
        self.size_range_select = SizeRangeSelect(driver)
        self.price_inputbox = PriceInputbox(driver)
        self.consumer_marketing_info_inputbox = ConsumerMarketingInfoInputbox(driver)
        self.retailer_marketing_info_inputbox = RetailerMarketingInfoInputbox(driver)
        self.save_button = SaveButton(driver)
        self.lead_time_inputbox = LeadTimeInputbox(driver)
        self.rrp_inputbox = RrpInputbox(driver)
        self.start_date_inputbox = StartDateInputbox(driver)
        self.expand_all_options_button = ExpandAllOptionsButton(driver)
        self.special_length_option_button = SpecialLengthOptionButton(driver)

    def set_size_range(self, lower, upper):
        required_size = '{0}-{1} (Size: {0} -> {1})'.format(lower, upper)

        if required_size not in self.size_range_select.options:
            raise ValueError("Could not select size '{} - {}'".format(lower, upper))

        self.size_range_select.selected = required_size

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