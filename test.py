from restaurant import Restaurant

test_restaurant = Restaurant(
    store_id=2979,
    city="Burnaby",
    address="4300 Kingsway #2170, Burnaby, BC"
)

test_restaurant.set_line_size(3)

print(test_restaurant)

print(test_restaurant.to_dict())