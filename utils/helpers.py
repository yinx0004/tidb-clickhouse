def append2file(filename, content):
    try:
        with open(filename, "a") as f:
            f.write(content)
    except Exception as err:
        raise Exception(err)


def fetch_in_brackets(str):
    start = str.find('(') + 1
    end = str.find(')', start)
    res = str[start:end] if start > 0 else None
    return res