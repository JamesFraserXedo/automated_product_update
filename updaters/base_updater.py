import imghdr
import os
import struct
import time
from selenium import webdriver
from selenium.webdriver.support.select import Select
from model.admin_page import AdminPage
from model.edit_product_page import EditProductPage
from model.header import Header
from model.impersonate_page import ImpersonatePage
from model.live_product_list_page import LiveProductListPage
from model.login_page import LoginPage
from product_types import ProductTypes
from StatusObject import StatusObject
from credentials import Credentials
from codec import *
from utils import Utils


class BaseUpdater:

    def __init__(self, customer_code):
        self.driver = webdriver.Firefox()
        self.login_page = LoginPage(self.driver)
        self.admin_page = AdminPage(self.driver)
        self.header = Header(self.driver)
        self.impersonate_page = ImpersonatePage(self.driver)
        self.live_product_list_page = LiveProductListPage(self.driver)

        self.customer_code = customer_code

        self.product_page = EditProductPage(self.driver)

    def impersonate(self):
        self.driver.get(Credentials.url)

        self.login_page.login(
            account_code=Credentials.account_code,
            user_name=Credentials.user_name,
            password=Credentials.password
        )

        self.admin_page.get_impersonate_button().click()

        self.impersonate_page.impersonate(self.customer_code)

    def update_product(self, product):
        status = OK
        messages = []

        self.header.get_live_products_button().click()

        self.live_product_list_page.filter_by_code(product.style)

        num_results = self.live_product_list_page.get_number_of_results(product.style)

        if num_results == 0:
            return self.handle_creation(product, messages)

        if num_results > 1:
            messages.append("More than one product with this code ({}) found".format(product.style))
            status = ERROR
            return StatusObject(status, messages)

        self.live_product_list_page.get_edit_product_button(product.style).click()

        if self.product_page.code_inputbox.text != product.style:
            messages.append("Attempted to update code {} , but accessed {} instead".format(product.style, self.product_page.code_inputbox.text))
            status = ERROR
            return StatusObject(status, messages)

        if self.product_page.collection_select.selected != product.collection:
            messages.append("Expected collection '{}' , but found '{}' instead".format(product.collection, self.product_page.collection_select.selected))
            status = ERROR
            return StatusObject(status, messages)

        if product.uk_size_range.replace(' ', '') not in self.product_page.size_range_select.options:
            messages.append("Expected size range {} , but found {} instead".format(product.uk_size_range, self.product_page.size_range_select.selected))
            status = ERROR
            return StatusObject(status, messages)

        current_uk_wholesale_price = self.product_page.price_inputbox.text
        if current_uk_wholesale_price != product.uk_wholesale_price:
            status = UPDATED
            self.product_page.price_inputbox.send_keys(str(round(product.uk_wholesale_price, 2)))
            messages.append("Updated price from £{} to £{}".format(round(current_uk_wholesale_price, 2), round(product.uk_wholesale_price, 2)))

        current_consumer_marketing_info = self.product_page.consumer_marketing_info_inputbox.text.replace('\r', ' ').replace('\n', ' ')
        current_retailer_marketing_info = self.product_page.retailer_marketing_info_inputbox.text.replace('\r', ' ').replace('\n', ' ')

        if product.marketing_info:
            if current_consumer_marketing_info == current_retailer_marketing_info == '':
                status = UPDATED
                self.product_page.consumer_marketing_info_inputbox.send_keys(product.marketing_info)
                messages.append("Added marketing info:")
                messages.append("\t{}".format(product.marketing_info))

            elif current_consumer_marketing_info != current_retailer_marketing_info:
                messages.append("Consumer and Retailer marketing info did not match before editing:")
                messages.append("\tConsumer: {}".format(current_consumer_marketing_info))
                messages.append("\tRetailer: {}".format(current_retailer_marketing_info))
                status = WARNING

            else:
                messages.append("Consumer and Retailer marketing already contain data:")
                messages.append("\t{}".format(current_consumer_marketing_info.replace('\r', ' ').replace('\n', ' ')))
                status = WARNING

        current_colours = self.product_page.get_current_colours()
        product_colours = [x.strip() for x in product.colours_available.split(',')]

        if sorted(current_colours) != sorted(product_colours):

            colour_messages = self.product_page.update_colours(product_colours)
            if len(colour_messages) == 0:
                status = UPDATED
            else:
                status = WARNING

            messages += colour_messages
            old_colours = current_colours
            current_colours = self.product_page.get_current_colours()
            if old_colours != current_colours:
                messages.append("Updated colours from {} to {}".format(old_colours, current_colours))

        self.product_page.save_button.click()

        return StatusObject(status, messages)

    def handle_creation(self, product, messages):
        path_to_image = self.get_path_to_image(product.style)[0]
        print(path_to_image)

        self.header.get_add_product_button().click()

        brand_select = Select(Utils.find_element_by_id_wait(self.driver, "BrandUnid"))
        brand_select.select_by_visible_text('Mori Lee')

        product_select = Select(Utils.find_element_by_id_wait(self.driver, "ProductTypeUnid"))
        if product.product_type == ProductTypes.MoriLee.BRIDESMAID_DRESS:
            product_select.select_by_visible_text('Bridesmaid Dress')
        elif product.product_type == ProductTypes.MoriLee.WEDDING_DRESS:
            product_select.select_by_visible_text('Wedding Dress')
        else:
            status = NEEDS_CREATED
            messages.append("Could not select product type {}".format(product.product_type))
            return StatusObject(status, messages)

        create_product_button = Utils.find_element_by_id_wait(self.driver, "CreateProductSingleButton")
        create_product_button.click()

        self.product_page.code_inputbox.text = product.style
        self.product_page.name_inputbox.text = product.style

        self.product_page.collection_select.selected = product.collection

        self.product_page.image_uploader.text = path_to_image

        # TODO
        # self.product_page.lead_time_inputbox

        self.product_page.price_inputbox.text = str(round(product.uk_wholesale_price, 2))

        # TODO
        # self.product_page.get_rrp_inputbox()

        self.product_page.set_size_range(product.size_lower, product.size_upper)
        self.product_page.update_colours(product.colours_available)

        if product.marketing_info:
            self.product_page.consumer_marketing_info_inputbox.text = product.marketing_info
            self.product_page.retailer_marketing_info_inputbox.text = product.marketing_info

            if product.marketing_info.contains('Available in 3 lengths - standard 61", 58" & 55"'):
                self.product_page.expand_all_options_button.click()
                self.product_page.special_length_option_button.click()

        time.sleep(10)
        status = NEEDS_CREATED
        return StatusObject(status, messages)
        quit()

        # self.product_page.save_button.click()

    def teardown(self):
        self.driver.quit()

    def get_path_to_image(self, code):
        base_dir = 'X:\Xedo Support\Bridal Designers Info\Mori Lee'

        preferred = None
        all_images = []
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                if file.startswith(code):
                    all_images.append(os.path.join(root, file))
                    if not preferred and self.is_portrait(os.path.join(root, file)):
                        preferred = os.path.join(root, file)
        if not preferred and len(all_images) > 0:
            preferred = all_images[0]
        return preferred, all_images

    def is_portrait(self, fname):
        sizes = self.get_image_size(fname)
        return sizes[0] < sizes[1]

    def get_image_size(self, fname):
        '''Determine the image type of fhandle and return its size.
        from draco'''
        with open(fname, 'rb') as fhandle:
            head = fhandle.read(24)
            if len(head) != 24:
                return
            if imghdr.what(fname) == 'png':
                check = struct.unpack('>i', head[4:8])[0]
                if check != 0x0d0a1a0a:
                    return
                width, height = struct.unpack('>ii', head[16:24])
            elif imghdr.what(fname) == 'gif':
                width, height = struct.unpack('<HH', head[6:10])
            elif imghdr.what(fname) == 'jpeg':
                try:
                    fhandle.seek(0)  # Read 0xff next
                    size = 2
                    ftype = 0
                    while not 0xc0 <= ftype <= 0xcf:
                        fhandle.seek(size, 1)
                        byte = fhandle.read(1)
                        while ord(byte) == 0xff:
                            byte = fhandle.read(1)
                        ftype = ord(byte)
                        size = struct.unpack('>H', fhandle.read(2))[0] - 2
                    # We are at a SOFn block
                    fhandle.seek(1, 1)  # Skip `precision' byte.
                    height, width = struct.unpack('>HH', fhandle.read(4))
                except Exception:  # IGNORE:W0703
                    return
            else:
                return
            return width, height