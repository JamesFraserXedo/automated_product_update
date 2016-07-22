import Tools
from model.locators import Locators
from model.object.elements import *
from model.object.base_page_object import BasePageObject
import Utils


class CodeInputbox(Inputbox):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=Locators.ProductForm.code_inputbox
        )


class NameInputbox(Inputbox):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=Locators.ProductForm.name_inputbox
        )


class CollectionSelect(Selector):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=Locators.ProductForm.collection_select
        )


class ImageUploader(Inputbox):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=Locators.ProductForm.image_uploader
        )


class SizeRangeSelect(Selector):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=Locators.ProductForm.size_range_select
        )


class PriceInputbox(Inputbox):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=Locators.ProductForm.price_inputbox
        )


class ConsumerMarketingInfoInputbox(Inputbox):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=Locators.ProductForm.consumer_marketing_info_inputbox
        )


class RetailerMarketingInfoInputbox(Inputbox):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=Locators.ProductForm.retailer_marketing_info_inputbox
        )


class SaveButton(Button):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=Locators.ProductForm.save_button
        )


class CancelButton(Button):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=Locators.ProductForm.cancel_button
        )


class LeadTimeInputbox(Inputbox):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=Locators.ProductForm.leadtime_inputbox
        )


class RrpInputbox(Inputbox):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=Locators.ProductForm.rrp_inputbox
        )


class StartDateInputbox(Inputbox):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=Locators.ProductForm.start_date_inputbox
        )


class ExpandAllOptionsButton(Button):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=Locators.ProductForm.expand_all_button
        )


class SpecialLengthOptionCheckbox(Checkbox):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=Locators.ProductForm.special_length_option
        )


class EditColoursButton(Button):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=Locators.ProductForm.edit_colours_button
        )


class EditProductPage(BasePageObject):
    def __init__(self, driver):
        super().__init__(driver, Locators.ProductForm.image_uploader)
        self.code_inputbox = CodeInputbox(driver)
        self.name_inputbox = NameInputbox(driver)
        self.collection_select = CollectionSelect(driver)
        self.image_uploader = ImageUploader(driver)
        self.size_range_select = SizeRangeSelect(driver)
        self.price_inputbox = PriceInputbox(driver)
        self.consumer_marketing_info_inputbox = ConsumerMarketingInfoInputbox(driver)
        self.retailer_marketing_info_inputbox = RetailerMarketingInfoInputbox(driver)
        self.save_button = SaveButton(driver)
        self.cancel_button = CancelButton(driver)
        self.lead_time_inputbox = LeadTimeInputbox(driver)
        self.rrp_inputbox = RrpInputbox(driver)
        self.start_date_inputbox = StartDateInputbox(driver)
        self.expand_all_options_button = ExpandAllOptionsButton(driver)
        self.special_length_option_checkbox = SpecialLengthOptionCheckbox(driver)
        self.edit_colours_button = EditColoursButton(driver)

    def set_size_range(self, lower, upper):
        required_size = '{0}-{1} (Size: {0} -> {1})'.format(lower, upper)

        if required_size not in self.size_range_select.options:
            raise ValueError("Could not select size '{} - {}'".format(lower, upper))

        self.size_range_select.selected = required_size

    @property
    def current_colours(self):
        colour_elements = Utils.find_elements_by(self.driver, Locators.ProductForm.selected_colours)
        colours = []
        for element in colour_elements:
            colours.append(element.text)
        return colours

    @property
    def current_colour_set(self):
        colour_elements = Utils.find_elements_by(self.driver, Locators.ProductForm.selected_colours)
        colours = []
        for element in colour_elements:
            colours.append(element.text.replace('*', '').split('(')[0].strip())
        return colours

    @property
    def consumer_marketing_info(self):
        contents = self.consumer_marketing_info_inputbox.text
        return Tools.split_on_new_line(contents)

    def append_consumer_marketing_info(self, text, status_object):
        text = Tools.new_line_per_sentence(text)
        text_items = Tools.split_on_new_line(text)

        old_contents = self.consumer_marketing_info
        new_contents = self.consumer_marketing_info

        for item in text_items:
            if item not in new_contents:
                new_contents.append(item)

        if old_contents != new_contents:
            self.consumer_marketing_info_inputbox.text = Tools.list_to_string(new_contents)

            status_object.old_consumer_comments = old_contents
            status_object.new_consumer_comments = new_contents


    @property
    def retailer_marketing_info(self):
        contents = self.retailer_marketing_info_inputbox.text
        return Tools.split_on_new_line(contents)

    def append_retailer_marketing_info(self, text, status_object):
        text = Tools.new_line_per_sentence(text)
        text_items = Tools.split_on_new_line(text)

        old_contents = self.retailer_marketing_info
        new_contents = self.retailer_marketing_info

        for item in text_items:
            if item not in new_contents:
                new_contents.append(item)

        if old_contents != new_contents:
            self.retailer_marketing_info_inputbox.text = Tools.list_to_string(new_contents)

            status_object.old_retailer_comments = old_contents
            status_object.new_retailer_comments = new_contents