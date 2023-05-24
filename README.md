# Travel-Recommendation-Project
Use the travel dataset which has three files’ users, flights, and hotels to build a recommendation system. 

1. `data()`: This function reads data from three CSV files containing information about users, flights, and hotels. It returns three data frames: `users`, `flights`, and `hotels`.

2. `using_datadata (user, budget, users, flights, hotels)`: This function filters flights and hotels data based on the user's code and calculates the cheapest flights and hotels for each city. It then merges the two data frames to get the total cost of visiting each city. It returns a data frame `city_costs` containing the total cost of visiting each city.

3. `dynamic_programming (budget, current_city, unvisited_cities, city_costs, memo)`: This function recursively calculates the maximum number of attractions the user can visit given their budget and the cities they have not yet visited. It uses memoization to avoid redundant calculations. It returns the maximum number of attractions the user can visit.

4. `generate_optimal_path (budget, current_city, unvisited_cities, city_costs, memo)`: This function recursively traces the optimal path the user should take to visit the maximum number of attractions. It also uses memoization to avoid redundant calculations. It returns a list of recommended cities to visit.

5. `list_recommendations(user, budget, num_cities)`: This function finds the starting city that maximizes the number of attractions the user can visit and then calls `trace_optimal_path` to generate the recommended cities to visit. It returns the starting city and a list of recommended cities to visit.
# The Algorithm
In this code, dynamic programming is used to optimize the process of finding the optimal path for a given user and budget. The dynamic_programming function uses memoization to store the results of previous computations, so that if the function is called again with the same parameters, it can return the previously computed result instead of recomputing it. This helps to avoid redundant computations and improve the efficiency of the algorithm.
The generate_optimal_path function also uses memoization to store the optimal path for a given user and budget. This function recursively calls itself to find the optimal path for each city in the unvisited cities set, and then returns the path with the maximum number of attractions.
The list_recommendations function uses the dynamic_programming and generate_optimal_path functions to find the optimal path for a given user and budget, and then returns the starting city and the recommended cities to visit based on the optimal path. By using dynamic programming techniques, this code is able to efficiently find the optimal path for a given user and budget, even for large datasets.

