import pandas as pd

def data():
    users = pd.read_csv('users.csv')
    flights = pd.read_csv('flights.csv')
    hotels = pd.read_csv('hotels.csv')
    return users, flights, hotels

def using_datadata(user, budget, users, flights, hotels):
    filtered_flights = flights[flights['userCode'] == user['code']]
    filtered_hotels = hotels[hotels['userCode'] == user['code']]

    cheapest_flights = filtered_flights.groupby(['from', 'to'])['price'].min().reset_index()
    cheapest_hotels = filtered_hotels.groupby('place')['total'].min().reset_index()

    city_costs = pd.merge(cheapest_flights, cheapest_hotels, left_on='to', right_on='place', how='left')
    city_costs['total_cost'] = city_costs['price'] + city_costs['total'].fillna(0)

    return city_costs

def dynamic_programming(budget, current_city, unvisited_cities, city_costs, memo):
    if budget <= 0 or not unvisited_cities:
        return 0

    if (current_city, tuple(unvisited_cities), budget) in memo:
        return memo[(current_city, tuple(unvisited_cities), budget)]

    max_attractions_count = 0
    for city in unvisited_cities:
        cost = city_costs.loc[(city_costs['from'] == current_city) & (city_costs['to'] == city), 'total_cost'].values
        if cost.size > 0 and budget >= cost[0]:
            new_unvisited_cities = unvisited_cities - {city}
            attractions_count = 1 + dynamic_programming(budget - cost[0], city, new_unvisited_cities, city_costs, memo)
            max_attractions_count = max(max_attractions_count, attractions_count)

    memo[(current_city, tuple(unvisited_cities), budget)] = max_attractions_count
    return max_attractions_count

def generate_optimal_path(budget, current_city, unvisited_cities, city_costs, memo):
    if budget <= 0 or not unvisited_cities:
        return []

    optimal_path = []
    max_attractions_count = 0
    for city in unvisited_cities:
        cost = city_costs.loc[(city_costs['from'] == current_city) & (city_costs['to'] == city), 'total_cost'].values
        if cost.size > 0 and budget >= cost[0]:
            new_unvisited_cities = unvisited_cities - {city}
            attractions_count = 1 + dynamic_programming(budget - cost[0], city, new_unvisited_cities, city_costs, memo)
            if attractions_count > max_attractions_count:
                max_attractions_count = attractions_count
                optimal_path = [city] + generate_optimal_path(budget - cost[0], city, new_unvisited_cities, city_costs, memo)

    return optimal_path

def list_recommendations(user, budget, num_cities):
    users, flights, hotels = data()
    city_costs =using_datadata(user, budget, users, flights, hotels)

    memo = {}
    max_attractions_count = 0
    optimal_path = []
    starting_city = None
    starting_cities = city_costs['from'].unique()
    for city in starting_cities:
        unvisited_cities = set(city_costs['to'].unique()) - {city}
        attractions_count = dynamic_programming(budget, city, unvisited_cities, city_costs, memo)
        if attractions_count > max_attractions_count:
            max_attractions_count = attractions_count
            starting_city = city
            optimal_path = generate_optimal_path(budget, city, unvisited_cities, city_costs, memo)

    recommendations = optimal_path[:num_cities]

    return starting_city, recommendations

# Example usage
user = {'code': 1}
budget = 2000
num_cities = 3
starting_city, recommendations = list_recommendations(user, budget, num_cities)
print(f"Starting city: {starting_city}")
print(f"Recommended cities to visit: {recommendations}")
assert recommendations == ['Recife (PE)', 'Brasilia (DF)']
print("Test case 1 passed")
assert len(recommendations)==2
print("Test case 2 passed")


