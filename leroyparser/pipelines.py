import scrapy
from itemadapter import ItemAdapter
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline


class LeroyParserPipeline:
    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.mongo_db = client.leroy

    def process_item(self, item, spider):
        item['params'] = dict(zip(item['param_key'], item['param_value']))
        del item['param_key'], item['param_value']

        collection = self.mongo_db[spider.name]
        collection.insert_one(item)
        # collection.update_one(item, {'$set': item}, upsert=True)
        return item


class LeroyParserImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item.get['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['photos'] = [itm[1] for itm in results if itm[0]]
        return item
