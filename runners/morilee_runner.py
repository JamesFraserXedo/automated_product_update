from codec import *
from loaders.other_loaders import VoyageLoader
from loaders.simple_loaders import MoriLeeLoader
from product_collections import Collections
from product_types import ProductTypes
from runners.base_runner import BaseRunner
from sheet_names import SheetNames


class MoriLeeRunner(BaseRunner):

    def __init__(self, filename):
        super().__init__(filename)

    customer_code = 'XMORILEE'

    sheets_to_update = [
        {
            COLLECTION: Collections.MoriLee.MORI_LEE_BRIDAL,
            PRODUCT_TYPE: ProductTypes.MoriLee.WEDDING_DRESS,
            LOADER: MoriLeeLoader(),
            SHEET_NAME: SheetNames.MoriLee.MAIN
        },
        # {
        #     COLLECTION: Collections.MoriLee.BLU_BRIDAL,
        #     PRODUCT_TYPE: ProductTypes.MoriLee.WEDDING_DRESS,
        #     LOADER: MoriLeeLoader(),
        #     SHEET_NAME: SheetNames.MoriLee.BLU
        # },
        # {
        #     COLLECTION: Collections.MoriLee.VOYAGE_COLLECTION,
        #     PRODUCT_TYPE: ProductTypes.MoriLee.WEDDING_DRESS,
        #     LOADER: VoyageLoader(),
        #     SHEET_NAME: SheetNames.MoriLee.VOYAGE
        # },
        # {
        #     COLLECTION: Collections.MoriLee.ANGELINA_FACCENDA_BRIDAL,
        #     PRODUCT_TYPE: ProductTypes.MoriLee.WEDDING_DRESS,
        #     LOADER: MoriLeeLoader(),
        #     SHEET_NAME: SheetNames.MoriLee.ANGELINA
        # },
        # {
        #     COLLECTION: Collections.MoriLee.JULIETTA,
        #     PRODUCT_TYPE: ProductTypes.MoriLee.WEDDING_DRESS,
        #     LOADER: MoriLeeLoader(),
        #     SHEET_NAME: SheetNames.MoriLee.JULIETTA
        # },
        # {
        #     COLLECTION: Collections.MoriLee.TULLE_AFFAIRS,
        #     PRODUCT_TYPE: ProductTypes.MoriLee.BRIDESMAID_DRESS,
        #     LOADER: MoriLeeLoader(),
        #     SHEET_NAME: SheetNames.MoriLee.TULLE_AFFAIRS
        # },
        # {
        #     COLLECTION: Collections.MoriLee.AFFAIRS,
        #     PRODUCT_TYPE: ProductTypes.MoriLee.BRIDESMAID_DRESS,
        #     LOADER: MoriLeeLoader(),
        #     SHEET_NAME: SheetNames.MoriLee.AFFAIRS
        # },


        # { # This needs checked for the Vizcaya / Valencia weirdness
        #     COLLECTION: Collections.MoriLee.Vizcaya,
        #     PRODUCT_TYPE: ProductTypes.MoriLee.BRIDESMAID_DRESS,
        #     LOADER: VizcayaLoader(),
        #     SHEET_NAME: SheetNames.MoriLee.Vizcaya
        # },
        # {
        #     COLLECTION: Collections.MoriLee.,
        #     PRODUCT_TYPE: ProductTypes.MoriLee.BRIDESMAID_DRESS,
        #     LOADER: MoriLeeLoader(),
        #     SHEET_NAME: SheetNames.MoriLee.STICKS
        # },
        # {
        #     COLLECTION: Collections.MoriLee.,
        #     PRODUCT_TYPE: ProductTypes.MoriLee.BRIDESMAID_DRESS,
        #     LOADER: MoriLeeLoader(),
        #     SHEET_NAME: SheetNames.MoriLee.PAPARAZZI_CONT
        # },
        # {
        #     COLLECTION: Collections.MoriLee.MORI_LEE_BRIDESMAIDS,
        #     PRODUCT_TYPE: ProductTypes.MoriLee.BRIDESMAID_DRESS,
        #     LOADER: MoriLeeLoader(),
        #     SHEET_NAME: SheetNames.MoriLee.ABM
        # },
        # {
        #     COLLECTION: Collections.MoriLee.ANGELINA_FACCENDA,
        #     PRODUCT_TYPE: ProductTypes.MoriLee.BRIDESMAID_DRESS,
        #     LOADER: MoriLeeLoader(),
        #     SHEET_NAME: SheetNames.MoriLee.AF_ABM
        # }
    ]