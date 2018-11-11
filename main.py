import itertools
from itertools import groupby
from operator import itemgetter
import time

import file_reader
import  file_parser


file_path = "TestFiles/client_product.txt" #"TestFiles/test_file.txt" #
file_content = file_reader.read(file_path)
content_matrix, client_product = file_parser.parse(file_content)
clients = content_matrix[0]
clients_unique = set(clients)
products = content_matrix[1]
products_unique = set(products)

products_occurrences = dict()
for product in products_unique:
    products_occurrences[product] = products.count(product)

clients_shopping_list = []

client_product.sort(key=itemgetter(0))
groups = groupby(client_product, itemgetter(0))

clients_shopping_list = [[key, sorted([item[1] for item in data])] for (key, data) in groups]


client_product.sort(key=itemgetter(1))
groups = groupby(client_product, itemgetter(1))
products_with_clients_that_bought_it = [[key, [item[0] for item in data]] for (key, data) in groups]

print(products_occurrences)


print('Clients: ', len(clients_unique))
print('Products: ', len(products_unique))

allow_levels = [50];

for allow_level in allow_levels:
    start_time = time.time()

    step = 1
    allowed_products = list()
    # L1
    print("L1")
    allowed_products.append(sorted([product for product, product_occurrence in products_occurrences.items()
                             if product_occurrence >= allow_level]))

    step = step + 1
    # L2
    print("L2")
    candidate_list = sorted(list(set(itertools.combinations(allowed_products[0], step))))

    # Shopping list from clients that bought more or equal than associate rule level
    clients_shopping_list = [client_shopping[1] for client_shopping in clients_shopping_list
                             if len(client_shopping[1]) >= step]
    end_time_L1 = time.time();

    # For those clients that bought more than rule level make combinations of shopping list of a customer
    # to ensure that .count(combination) will be able to count sub-lists of shopping-list
    print("Combination1")
    list_to_make_combinations_of = [client_shopping for client_shopping in clients_shopping_list
                                    if len(client_shopping) > step]

    shopping_list_with_all_possible_combinations = list()
    for shopping_list in list_to_make_combinations_of:
        shopping_list_with_all_possible_combinations.append(sorted(list(set(itertools.combinations(shopping_list,
                                                                                                   step)))))
    list_not_to_make_combinations_of = [client_shopping for client_shopping in clients_shopping_list
                                        if len(client_shopping) == step]
    print("Combination2")
    if len(list_not_to_make_combinations_of) == 1:
        shopping_list_with_all_possible_combinations = [list(y) for x in shopping_list_with_all_possible_combinations
                                                        for y in x]
        shopping_list_with_all_possible_combinations = shopping_list_with_all_possible_combinations + \
                                                       list_not_to_make_combinations_of
    else:
        shopping_list_with_all_possible_combinations = shopping_list_with_all_possible_combinations + \
                                                       list_not_to_make_combinations_of
        shopping_list_with_all_possible_combinations = [item for item in shopping_list_with_all_possible_combinations
                                                    if len(item) == step]

    shopping_list_with_all_possible_combinations = sorted(list(shopping_list_with_all_possible_combinations))

    print("CombinationFinal")
    candidate_list_occurrences = dict()
    for combination in candidate_list:
        candidate_list_occurrences[combination] = shopping_list_with_all_possible_combinations.count(list(combination))

    #print(max(candidate_list_occurrences.items(), key=itemgetter(1))[0])
    #print(candidate_list_occurrences[max(candidate_list_occurrences.items(), key=itemgetter(1))[0]])
    allowed_products.append([pair for pair, candidate_set_occurrence in candidate_list_occurrences.items()
                            if candidate_set_occurrence >= allow_level])
    end_time_L2 = time.time();

    # L3
    print("L3")
    # Pick all allowed L2's and at third place add another value (that is present in all L2's values,
    # but is not duplicate)
    candidate_list_L3 = allowed_products[1]
    all_values_in_L2 = set([y for x in candidate_list_L3 for y in x])
    combination_for_L3 = []
    for item in candidate_list_L3:
        for sub_combination in all_values_in_L2:
            if sub_combination not in item:
                sub_item = [element for element in item]
                sub_item = sub_item + list(sub_combination)
                combination_for_L3.append(sorted(sub_item))
    combination_for_L3 = sorted(set(map(tuple, sorted(combination_for_L3))))

    # Check if elements of candidate list appear more than allow_level in clients shopping list
    step = step + 1

    list_to_make_combinations_of = [client_shopping for client_shopping in clients_shopping_list
                                    if len(client_shopping) > step]

    shopping_list_with_all_possible_combinations = []
    for shopping_list in list_to_make_combinations_of:
        shopping_list_with_all_possible_combinations.append(sorted(list(set(itertools.combinations(shopping_list,
                                                                                                   step)))))
    shopping_list_with_all_possible_combinations = sorted(shopping_list_with_all_possible_combinations)
    list_not_to_make_combinations_of = [client_shopping for client_shopping in clients_shopping_list
                                        if len(client_shopping) == step]

    if len(list_not_to_make_combinations_of) == 1:
        shopping_list_with_all_possible_combinations = [list(y) for x in shopping_list_with_all_possible_combinations
                                                        for y in x]
        shopping_list_with_all_possible_combinations = shopping_list_with_all_possible_combinations + \
                                                       list_not_to_make_combinations_of
    else:
        list_not_to_make_combinations_of = [tuple(item) for item in list_not_to_make_combinations_of]
        shopping_list_with_all_possible_combinations = [y for x in shopping_list_with_all_possible_combinations
                                                        for y in x]
        shopping_list_with_all_possible_combinations = shopping_list_with_all_possible_combinations + \
                                                       list_not_to_make_combinations_of
        shopping_list_with_all_possible_combinations = [item for item in shopping_list_with_all_possible_combinations
                                                        if len(item) == step]

        shopping_list_with_all_possible_combinations = sorted(list(shopping_list_with_all_possible_combinations))
        candidate_list_occurrences = dict()
        for combination in combination_for_L3:
            candidate_list_occurrences[combination] = shopping_list_with_all_possible_combinations.count(
                                                        combination)
        allowed_products.append([three for three, candidate_set_occurrence in candidate_list_occurrences.items()
                            if candidate_set_occurrence >= allow_level])

print(allowed_products[0])
print(allowed_products[1])
print(allowed_products[2])
    end_time = time.time()
