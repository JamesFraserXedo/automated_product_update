from model.locators import Locators
from model.object.base_page_object import BasePageObject
from model.object.elements import *


class DeselectAllButton(Button):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=Locators.ColourPalette.deselect_all_button
        )


class ColourSelect(Selector):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=Locators.ColourPalette.colour_select
        )


class SelectHighlightedButton(Button):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=Locators.ColourPalette.select_highlighted_button
        )


class SaveButton(Button):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=Locators.ColourPalette.save_button
        )


class ColourSetSelect(Selector):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=Locators.ColourPalette.colour_set_select
        )


class AdColourSetButton(Button):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            locator=Locators.ColourPalette.add_colour_set_button
        )


class ColourPalette(BasePageObject):
    def __init__(self, driver):
        self.driver = driver
        self.deselect_all_button = DeselectAllButton(driver)
        self.colour_select = ColourSelect(driver)
        self.select_highlighted_button = SelectHighlightedButton(driver)
        self.save_button = SaveButton(driver)
        self.colour_set_select = ColourSetSelect(driver)
        self.add_colour_set_button = AdColourSetButton(driver)

    def update_colours(self, colours, status_object):
        messages = []

        self.deselect_all_button.click()

        if type(colours) is str:
            new_colours = [x.strip() for x in colours.split(',')]
            colours = new_colours

        for colour in colours:
            try:
                self.colour_select.selector.deselect_all()
                self.colour_select.selector.select_by_visible_text(colour)
                self.select_highlighted_button.click()
            except:
                messages.append("Could not add colour {}".format(colour))
                status_object.requires_colour(colour)

        self.save_button.click()
        return messages

    def update_colour_set(self, colour_set, status_object):
        if type(colour_set) == list:
            colour_set = colour_set[0]
        messages = []

        self.deselect_all_button.click()

        try:
            self.colour_select.selector.select_by_visible_text(colour_set)
            self.add_colour_set_button.click()
        except:
            messages.append("Could not add colour set {}".format(colour_set))
            status_object.requires_colour_set(colour_set)

        self.save_button.click()
        return messages