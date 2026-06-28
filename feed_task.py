"""

RefList:
- https://barakaev.ru/feedchecker
- https://www.w3schools.com/xml/xml_syntax.asp

"""

from datetime import datetime


def offer_product_is_active(product, categories) -> bool:
    return bool(product["is_active"])


def offer_product_has_name(product, categories) -> bool:
    name = product["name"]
    if not name:
        return False

    name = name.strip()
    if not name:
        return False

    return True


def offer_product_has_picture(product, categories) -> bool:
    picture = product["image_url"]
    if not picture:
        return False

    picture = picture.strip()
    if not picture:
        return False

    if not any((
        picture.startswith("http://"),
        picture.startswith("https://"),
    )):
        return False

    return True


def offer_product_has_valid_price(product, categories) -> bool:
    price = product["price"]
    if not price:
        return False

    price = price.strip()
    if not price:
        return False

    try:
        price = float(price)
    except ValueError:
        return False

    if price <= 0.0:
        return False

    return True


def offer_product_category_is_active(product, categories) -> bool:
    product_category = None

    for category in categories:
        if product["category_id"] == category["id"]:
            product_category = category
            break

    if not product_category:
        return False

    if not product_category["is_active"]:
        return False

    return True


def document_escape_special_chars(value):
    CHARACTER_TO_ENTITY_REFERENCE_MAP = {
        "<": "&lt;",
        ">": "&gt;",
        "&": "&amp;",
        "\'": "&apos;",
        "\"": "&quot;",
    }
    for char, entity in CHARACTER_TO_ENTITY_REFERENCE_MAP.items():
        value = value.replace(char, entity)
    return value


def build_yml(products, categories, generated_at) -> str:
    xml = '<?xml version="1.0" encoding="UTF-8"?>'

    xml += f'<yml_catalog date="{generated_at}">'
    xml += "<shop>"

    xml += "<name>Test Shop</name>"
    xml += "<company>Test Company</company>"
    xml += "<url>https://example.test</url>"

    xml += '<currencies><currency id="RUB" rate="1"/></currencies>'

    offer_validators = [
        offer_product_is_active,
        offer_product_has_name,
        offer_product_has_picture,
        offer_product_has_valid_price,
        offer_product_category_is_active,
    ]

    products_categories_ids = set()
    xml += "<offers>"

    for product in sorted(
        products,
        key=lambda product: product["id"],
    ):
        if not all((
            [
                validator(product=product, categories=categories)
                for validator in offer_validators
            ]
        )):
            continue

        products_categories_ids.add(product["category_id"])

        xml += '<offer id="{product_id}" available="{available}">'.format(
            product_id=product["id"],
            available="true" if product["stock"] else "false",
        )

        xml += f"<url>https://example.test/products/{product['slug']}/</url>"

        price = product["price"].replace(".", ",")

        xml += f"<price>{price}</price>"

        product_price = float(product["price"])
        product_old_price = product.get("old_price") or "0"

        try:
            product_old_price = float(product_old_price)
        except ValueError:
            product_old_price = 0.0

        if product_old_price > product_price:
            xml += f"<oldprice>{product['old_price']}</oldprice>"

        xml += "<currencyId>RUB</currencyId>"
        xml += f"<categoryId>{product['category_id']}</categoryId>"
        xml += f"<picture>{product['image_url']}</picture>"
        xml += "<name>{product_name}</name>".format(
            product_name=document_escape_special_chars(
                value=product['name'],
            ),
        )

        if product["description"]:
            xml += "<description>{product_description}</description>".format(
                product_description=document_escape_special_chars(
                    value=product['description'],
                ),
            )

        xml += "</offer>"

    xml += "</offers>"
    xml += "<categories>"

    for category in sorted(
        categories,
        key=lambda category: category["id"],
    ):
        if category["id"] not in products_categories_ids:
            continue
        xml += '<category id="{category_id}">{category_name}</category>'.format(
            category_id=category["id"],
            category_name=document_escape_special_chars(
                value=category["name"],
            )
        )

    xml += "</categories>"
    xml += "</shop>"
    xml += "</yml_catalog>"

    return xml


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


if __name__ == "__main__":
    result = build_yml(
        products=PRODUCTS,
        categories=CATEGORIES,
        generated_at=datetime(2026, 6, 18, 12, 0),
    )
    # print(result)

    with open("test.yml", "w") as ftw:
        ftw.write(result)
