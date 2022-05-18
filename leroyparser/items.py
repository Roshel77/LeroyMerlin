import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def price_corr(value):
    value = int(value.split(".")[0])
    return value


def clear_values(values_list):
    new_value = [item.replace('\n', '').strip() for item in values_list]
    return new_value


def resize_img(value: str):
    return value.replace("w_1200,h_1200", "w_2000,h_2000")


class LeroyparserItem(scrapy.Item):
    _id = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(price_corr))
    images = scrapy.Field(input_processor=MapCompose(resize_img))
    specifications = scrapy.Field()
    param_key = scrapy.Field(input_processor=MapCompose(clear_values))
    param_value = scrapy.Field(input_processor=MapCompose(clear_values))

