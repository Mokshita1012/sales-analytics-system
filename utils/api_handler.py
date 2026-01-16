import requests


def fetch_all_products():
    """
    Retrieves the complete list of products
    from the DummyJSON Products API.

    The limit is set to 100 so that all
    available products are fetched in a single request.
    """

    url = "https://dummyjson.com/products?limit=100"

    try:
        response = requests.get(url)

        # Raises an error automatically if the request was unsuccessful
        response.raise_for_status()

        data = response.json()

        print("Products fetched successfully from the API")

        # Extract and return only the products list from the response
        return data.get("products", [])

    except requests.exceptions.RequestException as e:
        # Handles errors such as network issues or server failures
        print("Error while calling the API:", e)
        return []


def create_product_mapping(api_products):
    """
    Builds a dictionary that links each product ID
    to its relevant details.

    Sample structure:
    {
        1: {
            'title': 'iPhone',
            'category': 'phones',
            'brand': 'Apple',
            'rating': 4.6
        }
    }
    """

    product_mapping = {}

    for product in api_products:
        product_id = product.get("id")

        product_mapping[product_id] = {
            "title": product.get("title"),
            "category": product.get("category"),
            "brand": product.get("brand"),
            "rating": product.get("rating")
        }

    return product_mapping
