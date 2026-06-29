"""

RefList:
- https://barakaev.ru/feedchecker
- https://www.w3schools.com/xml/xml_syntax.asp

"""

from datetime import datetime
import xml.etree.ElementTree as ET


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


def build_yml(products, categories, generated_at: datetime) -> str:
    xml = ET.Element(
        "yml_catalog",
        date=generated_at.strftime("%Y-%m-%d %H:%M"),
    )

    elem_shop = ET.SubElement(xml, "shop")

    ET.SubElement(elem_shop, "name").text = "Test Shop"
    ET.SubElement(elem_shop, "company").text = "Test Company"
    ET.SubElement(elem_shop, "url").text = "https://example.test"

    elem_shop_currencies = ET.SubElement(elem_shop, "currencies")
    ET.SubElement(
        elem_shop_currencies,
        "currency",
        id="RUB",
        rate="1",
    )

    offer_validators = [
        offer_product_is_active,
        offer_product_has_name,
        offer_product_has_picture,
        offer_product_has_valid_price,
        offer_product_category_is_active,
    ]

    products_categories_ids = set()

    elem_shop_offers = ET.SubElement(elem_shop, "offers")

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

        elem_shop_offer = ET.SubElement(
            elem_shop_offers,
            "offer",
            id=str(product["id"]),
            available="true" if product["stock"] else "false",
        )

        ET.SubElement(
            elem_shop_offer,
            "url",
        ).text = f"https://example.test/products/{product['slug']}/"
        ET.SubElement(
            elem_shop_offer,
            "price",
        ).text = product["price"].replace(".", ",")

        product_price = float(product["price"])
        product_old_price = product.get("old_price") or "0"

        try:
            product_old_price = float(product_old_price)
        except ValueError:
            product_old_price = 0.0

        if product_old_price > product_price:
            ET.SubElement(
                elem_shop_offer,
                "oldprice",
            ).text = product['old_price']

        ET.SubElement(elem_shop_offer, "currencyId").text = "RUB"
        ET.SubElement(
            elem_shop_offer,
            "categoryId"
        ).text = str(product['category_id'])
        ET.SubElement(elem_shop_offer, "picture").text = product['image_url']
        ET.SubElement(elem_shop_offer, "name").text = product['name']

        if product["description"]:
            ET.SubElement(
                elem_shop_offer,
                "description"
            ).text = product['description']

    elem_shop_categories = ET.SubElement(elem_shop, "categories")

    for category in sorted(
        categories,
        key=lambda category: category["id"],
    ):
        if category["id"] not in products_categories_ids:
            continue

        ET.SubElement(
            elem_shop_categories,
            "category",
            id=str(category["id"]),
        ).text = category["name"]

    return ET.tostring(
        element=xml,
        encoding="UTF-8",
        xml_declaration=True,
    ).decode()


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

    with open("test_et_finale.yml", "w") as ftw:
        ftw.write(result)
