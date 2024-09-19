import random

import requests

session = requests.Session()

# Границы России по широте и долготе
MIN_LAT, MAX_LAT = 41.0, 81.0
MIN_LON, MAX_LON = 19.0, 169.0


# Функция генерации случайных координат в пределах России
def generate_random_coordinates():
    latitude = random.uniform(MIN_LAT, MAX_LAT)
    longitude = random.uniform(MIN_LON, MAX_LON)
    return round(latitude, 6), round(longitude, 6)


# Функция обновления координат для записей без них
def update_coordinates():
    for i in range(1, 134):
        latitude, longitude = generate_random_coordinates()

        session.post(
            f"http://localhost:8000/api/v1/marks/",
            json={
                "latitude": latitude,
                "longitude": longitude,
            },
            files={"image": open(f"images/{i}.jpg", "rb")},
        )

        print(f"Updated image {i} with latitude {latitude} and longitude {longitude}")


update_coordinates()
