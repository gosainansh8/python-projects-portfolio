"""
Program Execution: python food_recommender_interactive.py restaurants.csv

Description: Interactive command-line interface for the restaurant recommender.
Allows users to progressively filter restaurants by multiple criteria including
distance, endorsements, and cuisine type through a conversational interface.
"""

from sys import argv
import food_recommender


def main():
    welcome_msg = (
        'Hello! Welcome to the Restaurant Recommender!\n'
        'Please type in a command to filter different places to eat.\n'
        'These filters will apply to each other until you \'reset\' them.\n\n'
        'You can type \'exit\' to exit or \'help\' for a list of commands')

    help_message = (
        '\t help - redisplay this help message\n'
        '\t list - list the current set of restaurants being considered\n'
        '\t reset - resets the list of restaurants and prints welcome message\n'
        '\t dist <N> - filters restaurants within distance N\n'
        '\t endorsements <N> - keep only restaurants with at least N endorsements\n'
        '\t cuisine - lists all available cuisine options\n'
        '\t cuisine <type> - keeps only restaurants of the specified cuisine\n'
        '\t top - keep only the most endorsed restaurant of each cuisine\n'
        '\t exit - exits the program')

    print(welcome_msg)

    if len(argv) < 2:
        print('ERROR: expected restaurant csv file name as command line arg')
        return

    restaurants = food_recommender.load_restaurant_csv(argv[1])
    print('\nInitial Restaurants:')
    print(restaurants)

    current_set = set(restaurants.keys())

    while True:
        command = input('> ')
        
        if command.startswith('h'):
            print(help_message)
            
        elif command == 'list':
            if current_set:
                print(sorted(current_set))
            else:
                print("No restaurants match current filters")
                
        elif command == 'reset':
            current_set = set(restaurants.keys())
            print(f"Reset to {len(current_set)} restaurants")
            
        elif command.startswith('dist '):
            tokens = command.split()
            if len(tokens) != 2:
                print("Invalid number of args, expected 2 for 'dist <N>'")
                continue

            try:
                dist = float(tokens[1])
            except Exception:
                print("<N> must be a number, e.g. 3.14")
                continue

            next_set = food_recommender.max_distance(restaurants, dist)
            current_set = current_set & next_set
            print(f"{len(current_set)} restaurants within {dist} km")

        elif command.startswith('endorsements '):
            tokens = command.split()
            if len(tokens) != 2:
                print("Invalid number of args, expected 2 for 'endorsements <N>'")
                continue

            try:
                min_rating = int(tokens[1])
            except Exception:
                print("<N> must be an integer, e.g. 5")
                continue

            next_set = food_recommender.min_endorsements(restaurants, min_rating)
            current_set = current_set & next_set
            print(f"{len(current_set)} restaurants with {min_rating}+ endorsements")

        elif command.startswith('cuisine'):
            tokens = command.split()
            if len(tokens) == 1:
                current_dict = {k: v for k, v in restaurants.items() 
                              if k in current_set}
                available_cuisines = food_recommender.get_cuisines(current_dict)
                print(f"Available cuisines: {sorted(available_cuisines)}")
                continue
            elif len(tokens) > 2:
                print("Invalid number of args. Use 1 or 2 args with 'cuisine'")
                continue

            cuisine = tokens[1]
            all_cuisines = food_recommender.get_cuisines(restaurants)
            if cuisine not in all_cuisines:
                print(f"\"{cuisine}\" is not a cuisine in the dataset")
                print(f"Available: {sorted(all_cuisines)}")
                continue

            next_set = food_recommender.filter_cuisine(restaurants, cuisine)
            current_set = current_set & next_set
            print(f"{len(current_set)} {cuisine} restaurants")
            
        elif command.startswith('top'):
            current_dict = {k: v for k, v in restaurants.items() 
                          if k in current_set}
            current_set = food_recommender.best_by_cuisine(current_dict)
            print(f"Narrowed to {len(current_set)} top restaurants (one per cuisine)")
            
        elif command == "exit":
            print("Thank you for using Restaurant Recommender!")
            break
            
        else:
            print(f"Unidentified command '{command}'")
            print("Type 'help' for a list of supported commands")


if __name__ == '__main__':
    main()