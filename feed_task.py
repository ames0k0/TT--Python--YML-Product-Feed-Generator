from datetime import datetime


CATEGORIES = [
    {
        "id": 1,
        "name": "Чай",
        "is_active": True,
    },
    {
        "id": 2,
        "name": "Посуда",
        "is_active": True,
    },
    {
        "id": 3,
        "name": "Подарочные наборы",
        "is_active": False,
    },
]


PRODUCTS = [
    {
        "id": 101,
        "name": 'Чай "Лес & травы" <сбор №1>',
        "slug": "les-i-travy",
        "category_id": 1,
        "price": "490.00",
        "old_price": "590.00",
        "stock": 12,
        "description": "Вкус: мята & чабрец > классический чай",
        "image_url": "https://example.test/media/tea-101.jpg",
        "is_active": True,
    },
    {
        "id": 102,
        "name": "Чайник стеклянный",
        "slug": "glass-teapot",
        "category_id": 2,
        "price": "1500.00",
        "old_price": "1400.00",
        "stock": 0,
        "description": "Стеклянный чайник объёмом 800 мл",
        "image_url": "https://example.test/media/teapot-102.jpg",
        "is_active": True,
    },
    {
        "id": 103,
        "name": "Скрытый товар",
        "slug": "hidden-product",
        "category_id": 1,
        "price": "350.00",
        "old_price": None,
        "stock": 5,
        "description": "Товар отключён администратором",
        "image_url": "https://example.test/media/product-103.jpg",
        "is_active": False,
    },
    {
        "id": 104,
        "name": "Пробник чая",
        "slug": "tea-sample",
        "category_id": 1,
        "price": "0.00",
        "old_price": None,
        "stock": 30,
        "description": "Бесплатный пробник",
        "image_url": "https://example.test/media/product-104.jpg",
        "is_active": True,
    },
    {
        "id": 105,
        "name": "Чашка фарфоровая",
        "slug": "porcelain-cup",
        "category_id": 2,
        "price": "700.00",
        "old_price": "900.00",
        "stock": 4,
        "description": "Фарфоровая чашка",
        "image_url": None,
        "is_active": True,
    },
    {
        "id": 106,
        "name": "Подарочный набор",
        "slug": "gift-set",
        "category_id": 3,
        "price": "2500.00",
        "old_price": "3000.00",
        "stock": 2,
        "description": "Товар находится в неактивной категории",
        "image_url": "https://example.test/media/product-106.jpg",
        "is_active": True,
    },
    {
        "id": 107,
        "name": "Чай улун молочный",
        "slug": "milk-oolong",
        "category_id": 1,
        "price": "700.50",
        "old_price": None,
        "stock": 3,
        "description": "",
        "image_url": "https://example.test/media/product-107.jpg",
        "is_active": True,
    },
]


def build_yml(products, categories, generated_at) -> str:
    xml = '<?xml version="1.0" encoding="UTF-8"?>'

    xml += f'<yml_catalog date="{generated_at}">'
    xml += "<shop>"

    xml += "<name>Test Shop</name>"
    xml += "<company>Test Company</company>"
    xml += "<url>https://example.test</url>"

    xml += '<currencies><currency id="RUB" rate="1"/></currencies>'

    xml += "<categories>"

    for product in products:
        category = next(
            category
            for category in categories
            if category["id"] == product["category_id"]
        )

        xml += f'<category id="{category["id"]}">{category["name"]}</category>'

    xml += "</categories>"
    xml += "<offers>"

    for product in products:
        if not product["is_active"]:
            continue

        for category in categories:
            if product["category_id"] == category["id"]:
                if category["is_active"]:
                    # print(category["id"], '--', category["name"])
                    break
        else:
            continue

        if not product["name"].strip():
            continue

        if float(product["price"].strip()) <= 0.0:
            continue

        if not product["image_url"]:
            continue
        if not (
            product["image_url"].strip().startswith("http://")
            or
            product["image_url"].strip().startswith("https://")
        ):
            continue

        # print('\n\n', product["id"], end=' ')
        xml += f'<offer id="{product["id"]}" available="{product["stock"]}">'

        xml += f"<url>https://example.test/products/{product['slug']}/</url>"

        price = product["price"].replace(".", ",")

        xml += f"<price>{price}</price>"

        if product["old_price"]:
            if float(product["old_price"]) != 0.0:
                if float(product["old_price"]) > float(product["price"]):
                    xml += f"<oldprice>{product['old_price']}</oldprice>"
                    print(product["price"], "::", product["old_price"])

        xml += "<currencyId>RUB</currencyId>"
        xml += f"<categoryId>{product['category_id']}</categoryId>"
        xml += f"<picture>{product['image_url']}</picture>"
        xml += f"<name>{product['name']}</name>"
        if product["description"]:
            xml += f"<description>{product['description']}</description>"
        else:
            print(">>NODESC>>", product["id"])
        xml += "</offer>"

    xml += "</offers>"
    xml += "</shop>"
    xml += "</yml_catalog>"

    return xml


if __name__ == "__main__":
    result = build_yml(
        products=PRODUCTS,
        categories=CATEGORIES,
        generated_at=datetime(2026, 6, 18, 12, 0),
    )
    print(result)
