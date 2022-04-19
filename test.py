import concurrent.futures
import time

import pandas as pd
from tqdm import tqdm


def timed_future_progress_bar(future, expected_time, increments=10):
    """
    Display progress bar for expected_time seconds.
    Complete early if future completes.
    Wait for future if it doesn't complete in expected_time.
    """
    interval = expected_time / increments
    with tqdm(total=increments) as pbar:
        for i in range(increments - 1):
            if future.done():
                # finish the progress bar
                # not sure if there's a cleaner way to do this?
                pbar.update(increments - i)
                return
            else:
                time.sleep(interval)
                pbar.update()
        # if the future still hasn't completed, wait for it.
        future.result()
        pbar.update()


def blocking_job():
    for i in range(100000000):
        a = 0
        b = a
        a += 1
        b = a


def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(blocking_job)
        timed_future_progress_bar(future, 5)

    print(f'Work done: {future.result()}')




candidats = ["Zemmour", "Macron", "Pécresse", "Mélenchon", "Jadot", "Dupont-Aignan", "Arthaud", "Hidalgo", "Poutou",
             "Le Pen", "Roussel", "Lassalle"]

candidats = sorted(candidats, reverse=True)

donnee = pd.read_csv("../nlp/csv/df_final.csv")

reponse_positive = []
reponse_negative = []
for choix in donnee['candidat']:
    if donnee['predicted'] == True:
        reponse_positive.append(choix)
    else:
        reponse_negative.append(choix)


apparition_positive = []
apparition_negative = []

for candidat in candidats:
    apparition_positive.append(donnee.loc[donnee['candidat'] == candidat]['predicted'].sum())
    apparition_negative.append((donnee.loc[donnee['candidat'] == candidat]['predicted'].count) - (donnee.loc[donnee['candidat'] == candidat]['predicted'].sum()))
