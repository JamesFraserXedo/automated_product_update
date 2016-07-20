from selenium.webdriver.common.by import By


class Locators:

    class ProductForm:
        code_inputbox = (By.ID, 'StagedProduct_Code')
        name_inputbox = (By.ID, 'StagedProduct_Caption')
        image_uploader = (By.ID, 'ImageUploadFile')
        collection_select = (By.ID, 'CollectionUnid')
        size_range_select = (By.XPATH, "//*[@class='size-templates-ddl']")
        price_inputbox = (By.XPATH, "//input[contains(@id, 'CostPrice')]")
        consumer_marketing_info_inputbox = (By.ID, 'StagedProduct_ConsumerMarketingInfo')
        retailer_marketing_info_inputbox = (By.ID, 'StagedProduct_MarketingInfo')
        save_button = (By.ID, 'SaveProduct')
        cancel_button = (By.XPATH, "//a[@title='Cancel']")
        leadtime_inputbox = (By.XPATH, "//input[contains(@id, 'LeadTime')]")
        rrp_inputbox = (By.XPATH, "//input[contains(@id, 'Rrp')]")
        start_date_inputbox = (By.XPATH, "//input[contains(@id, 'StartDatepicker')]")
        edit_colours_button = (By.XPATH, "EditColours")
        deselect_all_button = (By.ID, 'DeselectAll')
        available_colours_select = (By.ID, 'AvailableIds')
        select_highlighted_button = (By.ID, 'SelectHighlighted')
        save_colours_button = (By.ID, 'SaveDialog')
        expand_all_button = (By.XPATH, "//*[@class='expandAll']")
        special_length_option = (By.XPATH, "//*[contains(text(), 'Special Length')]/../input")
        edit_colours_button = (By.ID, "EditColours")
        selected_colours = (By.XPATH, "//span[@class='pgtoListItem']")

    class AdminPage:
        impersonate_button = (By.XPATH, "//a[@title='Impersonate']/..")

    class Header:
        add_product_button = (By.XPATH, "//a[text()='Add Product']")
        live_products_button= (By.XPATH, "//a[text()='Live Products']")

    class ImpersonatePage:
        customer_code_inputbox = (By.XPATH, "//*[@class='custom-combobox-input ui-widget ui-widget-content ui-state-default ui-corner-left ui-autocomplete-input']")
        select_retailer_button = (By.ID, "select-retailer")
        impersonate_button = (By.XPATH, "//*[@class='btnLogin button']")
        first_result = (By.XPATH, "//*[@id='ui-id-1']/li")

    class LiveProductListPage:
        code_filter_button = (By.XPATH, "//*[@data-title='Code']//span[@class='k-icon k-filter']")
        filter_inputbox = (By.XPATH, "//input[@class='k-textbox']")
        activate_filter_button = (By.XPATH, "//button[@type='submit']")

    class LoginPage:
        account_code_inputbox = (By.ID, "AccountCode")
        user_name_inputbox = (By.ID, "UserName")
        password_inputbox = (By.ID, "Password")
        login_button = (By.XPATH, "//*[@class='commonButton inputButton']")

    class ColourPalette:
        deselect_all_button = (By.ID, "DeselectAll")
        colour_select = (By.ID, "AvailableIds")
        select_highlighted_button = (By.ID, "SelectHighlighted")
        save_button = (By.ID, "SaveDialog")
        colour_set_select = (By.ID, "ColourSet")
        add_colour_set_button = (By.ID, "AddColourSet")