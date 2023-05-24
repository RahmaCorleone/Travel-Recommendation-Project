import pandas as pd

def data():
    users = pd.read_csv('users.csv')
    flights = pd.read_csv('flights.csv')
    hotels = pd.read_csv('hotels.csv')
    return users, flights, hotels

def get_city_costs(user, flights, hotels):
    filtered_flights = flights[flights['userCode'] == user['code']]
    filtered_hotels = hotels[hotels['userCode'] == user['code']]

    cheapest_flights = filtered_flights.groupby(['from', 'to'])['price'].min().reset_index()
    cheapest_hotels = filtered_hotels.groupby('place')['total'].min().reset_index()

    city_costs = pd.merge(cheapest_flights, cheapest_hotels, left_on='to', right_on='place', how='left')
    city_costs['total_cost'] = city_costs['price'] + city_costs['total'].fillna(0)

    return city_costs

def max_attractions(budget, current_city, unvisited_cities, city_costs, memo):
    if budget <= 0 or not unvisited_cities:
        return 0, []

    if (current_city, tuple(unvisited_cities), budget) in memo:
        return memo[(current_city, tuple(unvisited_cities), budget)]

    max_count = 0
    best_cities = []
    for city in unvisited_cities:
        cost = city_costs.loc[(city_costs['from'] == current_city) & (city_costs['to'] == city), 'total_cost'].values
        if cost.size > 0 and budget >= cost[0]:
            new_unvisited_cities = unvisited_cities - {city}
            count, visited_cities = max_attractions(budget - cost[0], city, new_unvisited_cities, city_costs, memo)
            count += 1
            if count > max_count:
                max_count = count
                best_cities = [city] + visited_cities

    memo[(current_city, tuple(unvisited_cities), budget)] = (max_count, best_cities)
    return max_count, best_cities
def list_recommendations(user, budget, num_cities):
    users, flights, hotels = data()
    city_costs = get_city_costs(user, flights, hotels)

    memo = {}
    max_count = 0
    starting_city = None
    best_cities = []
    starting_cities = city_costs['from'].unique()
    for city in starting_cities:
        unvisited_cities = set(city_costs['to'].unique()) - {city}
        count, visited_cities = max_attractions(budget, city, unvisited_cities, city_costs, memo)
        if count > max_count:
            max_count = count
            starting_city = city
            best_cities = visited_cities

    return starting_city, max_count, best_cities

# Example usage
user = {'code': 1}
budget = 3000
num_cities = 3
starting_city, max_attractions_count, recommended_cities = list_recommendations(user, budget, num_cities)
print(f"Starting city: {starting_city}")
print(f"Recommended cities: {', '.join(recommended_cities)}")
print(f"Max number of attractions: {max_attractions_count}")
assert recommended_cities == ['Recife (PE)', 'Brasilia (DF)', 'Florianopolis (SC)']
print("Test case 1 passed")
assert len(recommended_cities)==3
print("Test case 2 passed")
