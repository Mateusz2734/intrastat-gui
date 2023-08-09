import pandas as pd


def get_columns(args):
    if len(args) != 1:
        raise Exception("Wrong number of arguments")

    path = args[0]

    data = pd.read_excel(path)

    return list(data.columns)


def duplicates(args):
    if len(args) != 2:
        raise Exception("Wrong number of arguments")

    path = args[0]
    column = args[1]

    data = pd.read_excel(path)

    data.drop_duplicates(subset=column, inplace=True)

    data.to_excel(path, index=False)
