import itertools
from itertools import groupby
from operator import itemgetter
import time
from collections import Counter

import file_reader
import file_parser
import plotting


def flatten_list(list_to_flat):
    return [list(y) for x in list_to_flat
            for y in x]


def update_shopping_list(only_shopping_list, allowed_products):
    # Cut from shopping list for each client that items that are not allowed
    temp_list = [list(filter(lambda x: x in allowed_products, sublist)) for sublist in only_shopping_list]
    return temp_list


def perform_combinations(only_shopping_list_updated, step):
    all_possible_sorted_combinations = list()
    for item in only_shopping_list_updated:
        all_possible_sorted_combinations.append(sorted(list(set(itertools.combinations(item, step)))))
    return all_possible_sorted_combinations


def get_candidate_list_allowed(flatten_list, allow_level, mode=0):
    if mode == 1:
        res = Counter(flatten_list)
    else:
        res = Counter(map(tuple, flatten_list))
    return [key for key, value in res.items() if value >= allow_level]


file_path = "TestFiles/client_product.txt"
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
only_shopping_list = [clients_shopping_list_item[1] for clients_shopping_list_item in clients_shopping_list]

print('Clients: ', len(clients_unique))
print('Products: ', len(products_unique))

allow_levels = list(range(1, 100)) + [75, 80, 90, 100, 150, 200, 250, 500]

text_file_name = "Output.txt"
csv_file_name = "OutputCSV.csv"
open(text_file_name, "w").close()
with open(csv_file_name, "w") as csv_file:
    csv_file.write("Cut level;L1_quantity;L1_Time;L2_quantity;L2_Time;L3_quantity;L3_Time;L4_quantity;L4_Time;"
                   "Summary_Time\n")

step = 0

for allow_level in allow_levels:
    start_time = time.time()

    allowed_products = list()
    end_time_list = list()
    # L1
    step = 1

    candidate_list_allowed = get_candidate_list_allowed(products, allow_level, 1)
    allowed_products.append(candidate_list_allowed)
    end_time_list.append(time.time())

    only_shopping_list_updated = update_shopping_list(only_shopping_list, allowed_products[0])

    for l_level in range(2, 5):
        step = step + 1

        # Make combinations for each shopping list foreach client
        all_possible_Ls = perform_combinations(only_shopping_list_updated, step)

        flatten_all_possible_Ls = flatten_list(all_possible_Ls)

        candidate_list_allowed = get_candidate_list_allowed(flatten_all_possible_Ls, allow_level)

        allowed_products.append(candidate_list_allowed)
        end_time_list.append(time.time())

    with open(text_file_name, "a") as text_file:
        text_file.write("Cut level: %s\nL1: %s\tTime: %s\nL2: %s\tTime: %s\nL3: %s\tTime: %s\nSummary time: %s\n"
                        % (str(allow_level), len(allowed_products[0]), str(end_time_list[0] - start_time),
                           len(allowed_products[1]), str(end_time_list[1] - end_time_list[0]), len(allowed_products[2]),
                           str(end_time_list[2] - end_time_list[1]), str(end_time_list[2] - start_time)))

    with open(csv_file_name, "a") as csv_file:
        csv_file.write("%s;%s;%s;%s;%s;%s;%s;%s;%s;%s\n" % (str(allow_level), len(allowed_products[0]),
                                                       str(end_time_list[0] - start_time), len(allowed_products[1]),
                                                       str(end_time_list[1] - end_time_list[0]),
                                                       len(allowed_products[2]),
                                                       str(end_time_list[2] - end_time_list[1]),
                                                       len(allowed_products[3]),
                                                       str(end_time_list[3] - end_time_list[2]),
                                                       str(end_time_list[3] - start_time)))

    print('Write to file performed %d' % allow_level)

allow_levels, L1_quant, L1_Times, L2_quant, L2_Times, L3_quant, L3_Times, L4_quant, L4_Times, summary_times = \
    file_parser.parse_results(file_content)
plotting.plot_x_y(allow_levels, L1_quant, "L1 quantity vs Allow levels", "Allow level", "L1_quantity",
                  "L1Q_vs_Allow_Level.png")
plotting.plot_x_y(allow_levels, L1_Times, "L1 times vs Allow levels", "Allow level", "L1_Time",
                  "L1T_vs_Allow_Level.png")
plotting.plot_x_y(allow_levels, L2_quant, "L2 quantity vs Allow levels", "Allow level", "L2_quantity",
                  "L2Q_vs_Allow_Level.png")
plotting.plot_x_y(allow_levels, L2_Times, "L2 times vs Allow levels", "Allow level", "L2_Time",
                  "L2T_vs_Allow_Level.png")
plotting.plot_x_y(allow_levels, L3_quant, "L3 quantity vs Allow levels", "Allow level", "L3_quantity",
                  "L3Q_vs_Allow_Level.png")
plotting.plot_x_y(allow_levels, L3_Times, "L3 times vs Allow levels", "Allow level", "L3_Time",
                  "L3T_vs_Allow_Level.png")
plotting.plot_x_y(allow_levels, L4_quant, "L4 quantity vs Allow levels", "Allow level", "L4_quantity",
                  "L4Q_vs_Allow_Level.png")
plotting.plot_x_y(allow_levels, L4_Times, "L4 times vs Allow levels", "Allow level", "L4_Time",
                  "L4T_vs_Allow_Level.png")
plotting.plot_x_y(allow_levels, L4_Times, "Summary times vs Allow levels", "Allow level", "Summary_Time",
                  "Summary_time_vs_Allow_Level.png")



print("All work done!")
