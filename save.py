import csv
import pandas as pd


def save_to_file(articles, name):
    '''
    it saves exctracted data from main.py
    '''
    file = open(f"./data/{name}.csv", mode="w")
    writer = csv.writer(file)
    writer.writerow(["name", "timeline", "post", "like", "comment", "url"])
    for arcticle in articles:
        writer.writerow(list(arcticle.values()))
    return


def add_to_file(articles, name):

    file = open(f"./data/{name}.csv", mode="a")
    writer = csv.writer(file)
    file.write("\n")
    for arcticle in articles:
        writer.writerow(list(arcticle.values()))

    df = pd.read_csv(
        f"./data/{name}.csv", engine='python')
    new_df = df.drop_duplicates(subset='post')
    new_df.to_csv(f"./data/{name}.csv", index=False)
    return
