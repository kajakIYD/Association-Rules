def parse(content):
    content = content.split('\n')
    content_matrix = []
    content_matrix.append([consumer.split(';')[0] for consumer in content[:len(content)]])
    content_matrix.append([product.split(';')[1] for product in content[:len(content)]])
    client_product = [client_with_product.split(';') for client_with_product in content]
    return content_matrix, client_product[0:len(client_product)]


def parse_results(content):
    content = content.split('\n')
    content = content[1:len(content) - 1]
    allow_levels = []
    L1_quant = []
    L1_Times = []
    L2_quant = []
    L2_Times = []
    L3_quant = []
    L3_Times = []
    L4_quant = []
    L4_Times = []
    summary_times = []
    all_content = [allow_levels, L1_quant, L1_Times, L2_quant, L2_Times, L3_quant, L3_Times, L4_quant, L4_Times,
                   summary_times]
    for line in content:
        line = line.split(";")
        for id in range(0, len(line)):
            all_content[id].append(float(line[id]))
    return all_content[0], all_content[1], all_content[2],all_content[3], all_content[4], all_content[5], \
           all_content[6], all_content[7], all_content[8], all_content[9]