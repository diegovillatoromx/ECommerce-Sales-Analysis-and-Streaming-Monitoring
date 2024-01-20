import pandas as pd
import random
import hashlib
import time
from datetime import datetime, timedelta

# Initial configuration data
cities = ['Bogotá', 'Medellín', 'Cali', 'Bucaramanga', 'Barranquilla']
products = ['Dell Laptop', 'HP Laptop', 'Lenovo Laptop', 'PlayStation', 'Xbox', 'Nintendo Switch']
purchase_statuses = ['COMPLETED', 'FAILED_CHECKOUT', 'FAILED_API_RESPONSE', 'INSUFFICIENT_FUNDS', 'USER_ERROR', 'FRAUD', 'COMPLETED']
sources = ['Facebook', 'Instagram', 'Organic', 'Twitter', 'Influencer_1', 'Influencer_2', 'Influencer_3', 'Influencer_4']
payment_methods = ['Credit Card', 'PSE', 'Cash', 'Nequi', 'Daviplata']

# Dictionary for city coordinates
city_coords = {
    'Bogotá': [(4.6516, -74.1263), (4.6620, -74.1347), (4.6476, -74.1019)],
    'Medellín': [(6.1633, -75.6053), (6.1778, -75.5914), (6.1981, -75.5734)],
    'Cali': [(3.4288, -76.5375), (3.4149, -76.5404), (3.4164, -76.5475)],
    'Bucaramanga': [(7.0999, -73.1073), (7.0724, -73.1053)],
    'Barranquilla': [(11.0142, -74.8275), (11.0040, -74.8355), (10.9906, -74.7888)]
}

# Define a list of real brands
real_brands = ['Samsung', 'Apple', 'Sony', 'Nike', 'Adidas', 'LG', 'Microsoft']

# Define a list of real categories
real_categories = ['Electronics', 'Clothing', 'Home Appliances', 'Sports', 'Footwear', 'Entertainment']

# Function to determine payment method based on the source
def get_payment_method(source, purchase_statuses, online_payments, in_store_payments):
    if source == 'Organic':
        payment = random.choice(in_store_payments)
        status = 'COMPLETED'
        order_type = 'IN_STORE'
    else:
        payment = random.choice(online_payments)
        status = random.choice(purchase_statuses)
        order_type = 'ONLINE'
    return payment, status, order_type

# Function to get coordinates based on the city
def get_coordinates(city, city_coords):
    return random.choice(city_coords[city])

# Function to generate purchase data
def generate_purchase_data(num_records):
    data = []
    for x in range(num_records):
        #date = (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d %H:%M:%S")
        date = (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat()
        product = random.choice(products)
        pricing = round(random.uniform(200, 2000), 2)
        commission = round(random.uniform(10, 200), 2)
        city = random.choice(cities)
        source = random.choice(sources)
        payment, status, order_type = get_payment_method(source, purchase_statuses, payment_methods, payment_methods)
        coords = get_coordinates(city, city_coords)
        brand = random.choice(real_brands)  # Choose a random real brand
        category = random.choice(real_categories)  # Choose a random real category

        purchase = {
            'purchase_ID': hashlib.sha256(f"{x} {product} {pricing} {commission} {date} {source} {status}".encode('utf-8')).hexdigest()[:10],
            'Product_name': product,
            'Pricing': str(pricing),
            'Commission': str(commission),
            'Revenue': str(round(pricing * commission, 2)),
            'Payment_Method': payment,
            'Status': status,
            'Order_Type': order_type,
            'City': city,
            'Latitude': str(coords[0]),
            'Longitude': str(coords[1]),
            'Source': source,
            'Brand': brand,
            'Category': category,
            'Created_at': date
        }
        data.append(purchase)
        time.sleep(random.uniform(0.1, 0.5))  # Simulate processing time

    return data