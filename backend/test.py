from restaurant import Restaurant

test_restaurant = Restaurant(
    store_id=2979,
    city="Burnaby",
    address="#7-4300 Kingsway, Burnaby, BC V5H 1Z8"
)

test_restaurant.set_line_size(3)

print(test_restaurant)

print(test_restaurant.to_dict())