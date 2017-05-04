import base64


def base64_encode(string_data):
    """
    :param string_data: Input string to base64 encode
    :return: base64 encoded input
    """
    value = base64.b64encode(bytes(string_data, encoding='utf8'))
    return str(value, encoding='utf-8')


def secret_parser(key):
    """
    :param key: The name of the variable you want a value of. Example: "Twitter.ConsumerKey"
    :return: The value of the key if it exists; else a blank string
    """
    secrets = tuple(open("secrets.txt", 'r'))
    value = ""  # Our return value

    for line in secrets:
        pieces = line.split("=")
        if pieces[0] == key:
            value = pieces[1].strip('\n\r')  # Get rid of CRLFs

    return value
