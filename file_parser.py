def parse(content):
    content = content.split('\n')
    content_matrix = []
    content_matrix.append([consumer.split(';')[0] for consumer in content[:len(content)-2]])
    content_matrix.append([product.split(';')[1] for product in content[:len(content)-2]])
    client_product = [client_with_product.split(';') for client_with_product in content]
    return content_matrix, client_product[0:len(client_product)]
