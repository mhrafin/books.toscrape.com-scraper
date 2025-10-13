# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        ## strip all whitespaces from strings
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != "description":
                value = adapter.get(field_name)
                adapter[field_name] = value.strip()

        ## Convert category and product type to Lowercase
        adapter["category"] = adapter["category"].lower()
        adapter["product_type"] = adapter["product_type"].lower()

        ## Clean price data
        price_keys = ["price", "price_excl_tax", "price_incl_tax"]
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = value.replace("£", "")
            adapter[field_name] = float(value)

        ## Extract availability from text
        availability_text = adapter.get("availability")
        split_text_array = availability_text.split("(")
        availability_array = split_text_array[1].split(" ")
        adapter["availability"] = int(availability_array[0])

        ## Convert reviews to integer
        adapter["num_reviews"] = int(adapter["num_reviews"])

        ## Convert Stars to Number
        star_value = adapter.get("stars").lower()
        if "one" in star_value:
            adapter["stars"] = int(1)

        if "two" in star_value:
            adapter["stars"] = int(2)

        if "three" in star_value:
            adapter["stars"] = int(3)

        if "four" in star_value:
            adapter["stars"] = int(4)

        if "five" in star_value:
            adapter["stars"] = int(5)

        return item
