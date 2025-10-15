# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2


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
        price_keys = ["price", "price_excl_tax", "price_incl_tax", "tax"]
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = value.replace("£", "")
            adapter[price_key] = float(value)

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


class SaveToPostgresPipeline:
    def __init__(self):
        hostname = "localhost"
        username = "scrapy_user"
        password = "scrapy_pass"
        database = "bookscrap"

        self.connection = psycopg2.connect(
            host=hostname, user=username, password=password, dbname=database
        )

        self.cur = self.connection.cursor()

        ## Create books table if none exists

        self.cur.execute("""
    CREATE TABLE IF NOT EXISTS books(
        id serial PRIMARY KEY, 
        url VARCHAR(255),
        title text,
        upc VARCHAR(255),
        product_type VARCHAR(255),
        price_excl_tax DECIMAL,
        price_incl_tax DECIMAL,
        tax DECIMAL,
        price DECIMAL,
        availability INTEGER,
        num_reviews INTEGER,
        stars INTEGER,
        category VARCHAR(255),
        description text
    )
    """)

    def process_item(self, item, spider):
        ## Define insert statement
        self.cur.execute(
            """ insert into books (
            url, 
            title, 
            upc, 
            product_type, 
            price_excl_tax,
            price_incl_tax,
            tax,
            price,
            availability,
            num_reviews,
            stars,
            category,
            description
            ) values (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
                )""",
            (
                item["url"],
                item["title"],
                item["upc"],
                item["product_type"],
                item["price_excl_tax"],
                item["price_incl_tax"],
                item["tax"],
                item["price"],
                item["availability"],
                item["num_reviews"],
                item["stars"],
                item["category"],
                str(item["description"]),
            ),
        )

        ## Execute insert of data into database
        self.connection.commit()
        return item

    def close_spider(self, spider):
        ## Close cursor & connection to database
        self.cur.close()
        self.connection.close()
