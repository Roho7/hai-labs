from sklearn.tree import DecisionTreeClassifier
import numpy as np

# Mock dataset: tourist attractions, restaurants, historical landmarks mapped to a sequence
X_train = np.array([[1, 0, 1], [1, 1, 0], [0, 1, 1]])  # 1 if present, 0 if absent
y_train = [
    1,
    2,
    3,
]  # 1: historical - tourist - restaurant, 2: tourist - restaurant - historical, 3: restaurant - historical - tourist

model = DecisionTreeClassifier()
model.fit(X_train, y_train)


def ml_structure(city_data):
    sequence = model.predict(
        [
            [
                1 if "tourist_attractions" in city_data else 0,
                1 if "restaurants" in city_data else 0,
                1 if "historical_landmarks" in city_data else 0,
            ]
        ]
    )[0]

    sections = {
        1: f"Historical Landmarks:\n{city_data.get('historical_landmarks', '')}",
        2: f"Tourist Attractions:\n{city_data.get('tourist_attractions', '')}",
        3: f"Recommended Restaurants:\n{city_data.get('restaurants', '')}",
    }

    return "\n\n".join([sections[i] for i in range(1, 4) if sequence == i])


city_info = {
    "tourist_attractions": "Eiffel Tower",
    "restaurants": "Le Jules Verne",
    "historical_landmarks": "Louvre Museum",
}

print(ml_structure(city_info))
