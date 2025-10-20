"""
Program Execution: python food_recommender.py restaurants.csv

Description: Functions for a food recommender system for restaurants.
Includes CSV loading; listing cuisines; filtering restaurants by distance,
endorsements, and cuisine; and identifying the most endorsed restaurant
for each cuisine.
"""

RestaurantInfo = tuple[str, int, float, int]


def load_restaurant_csv(filename: str) -> dict[str, RestaurantInfo]:
    """
    Description: Loads restaurant data from a CSV file. Returns a dictionary
    mapping restaurant names to tuples containing the cuisine, price level,
    distance and number of endorsements for that restaurant.
    Input: str, representing the name of a file containing restaurant data
    Output: dictionary of tuples representing restaurants
    """

    file = open(filename, "r")
    lines = file.readlines()
    file.close()

    res = {}

    for i in lines[1:]:
        data = i.strip()
        split_data = data.split(",")
        name = split_data[0].strip()
        cuisine = split_data[1].strip()
        price = split_data[2].strip().count("$")
        distance = float(split_data[3].strip())
        endorsements = int(split_data[4].strip())
        res[name] = (cuisine, price, distance, endorsements)
    return res


def get_cuisines(restaurants: dict[str, RestaurantInfo]) -> set[str]:
    """
    Description: Returns set of all cuisine names in the restaurant data.
    Input: restaurants dict mapping name to restaurant characteristics
    Output: Set of cuisine strings
    """

    cuisines = set()
    for i in restaurants:
        restaurant_info = restaurants[i]
        cuisines.add(restaurant_info[0])
    return cuisines


def max_distance(
    restaurants: dict[str, RestaurantInfo], dist: float
) -> set[str]:
    """
    Description: Returns the names of restaurants with a distance less than
    or equal to the distance inputted.
    Input: restaurants dict and distance float
    Output: set of restaurant names within the specified distance
    """

    distance = set()
    for i in restaurants:
        distance_info = restaurants[i]
        if distance_info[2] <= dist:
            distance.add(i)
    return distance


def min_endorsements(
    restaurants: dict[str, RestaurantInfo], min_rating: int
) -> set[str]:
    """
    Description: Returns restaurants with endorsements at or above the
    entered minimum rating value.
    Input: restaurants dict and minimum rating int
    Output: set of restaurants that meet the minimum endorsement threshold
    """

    endorsements = set()
    for i in restaurants:
        endorsement_info = restaurants[i]
        if endorsement_info[3] >= min_rating:
            endorsements.add(i)
    return endorsements


def filter_cuisine(
    restaurants: dict[str, RestaurantInfo], cuisine: str
) -> set[str]:
    """
    Description: Returns the restaurant names that match the specified cuisine.
    Input: restaurants dict and cuisine string
    Output: restaurant names set that match the entered cuisine
    """

    filter_set = set()
    for i in restaurants:
        cuisine_info = restaurants[i]
        if cuisine_info[0].lower() == cuisine.lower():
            filter_set.add(i)
    return filter_set


def best_by_cuisine(
    restaurants: dict[str, RestaurantInfo],
) -> set[str]:
    """
    Description: Identifies the restaurant with the most endorsements for
    each cuisine and returns a set with those names.
    Input: restaurants dict with restaurant info
    Output: restaurant names set with most endorsed per cuisine
    """

    diverse = {}
    for i in restaurants:
        best_info = restaurants[i]
        cuisine = best_info[0]
        endorsements = best_info[3]
        if cuisine not in diverse:
            diverse[cuisine] = (i, endorsements)
        else:
            best_now = diverse[cuisine]
            endorsement_now = best_now[1]
            if endorsements > endorsement_now:
                diverse[cuisine] = (i, endorsements)

    result = set()
    for j in diverse:
        best_restaurant = diverse[j]
        restaurant_name = best_restaurant[0]
        result.add(restaurant_name)
    return result


def main():
    """
    Description: Loads restaurant data and demonstrates various filtering
    and recommendation operations.
    Input: CSV filename from command line
    Output: Filtered and recommended restaurants
    """

    import sys

    if len(sys.argv) < 2:
        print("Usage: python food_recommender.py <restaurants.csv>")
        return

    filename = sys.argv[1]
    restaurants = load_restaurant_csv(filename)

    print("Available cuisines:", get_cuisines(restaurants))
    print("\nRestaurants within 1.5 km:", max_distance(restaurants, 1.5))
    print("Restaurants with 5+ endorsements:", min_endorsements(restaurants, 5))
    print("Best restaurant per cuisine:", best_by_cuisine(restaurants))


if __name__ == "__main__":
    main()