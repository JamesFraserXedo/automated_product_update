from selenium.webdriver.common.by import By


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

    selected_colours = (By.XPATH, "//span[@class='pgtoListItem']")
