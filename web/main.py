import io
import os
import random
from flask import render_template, Response, Flask, request
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import base64
import pandas as pd

from nlp.main import predict_tweets_user, create_model
from scrapping.scrapping import scraping_user

app = Flask(__name__)


@app.route('/')
def view_home():
    return render_template("index.html", title="Home")


@app.route("/avis")
def avis():
    plot = plt
    # Generate the figure **without using pyplot**.

    donnee = pd.read_csv("../scrapping/csv/candidats/df_final.csv", index_col=0)
    donnee = donnee.loc[donnee['candidat'] != 'None']

    candidats = donnee['candidat'].unique()

    candidats = sorted(candidats, reverse=True)

    apparition_positive = []
    apparition_negative = []

    for candidat in candidats:
        apparition_positive.append(donnee.loc[donnee['candidat'] == candidat]['predicted'].sum())
        apparition_negative.append((donnee.loc[donnee['candidat'] == candidat]['predicted'].count()) - (
            donnee.loc[donnee['candidat'] == candidat]['predicted'].sum()))

    print(apparition_positive)
    print(apparition_negative)

    positif = plot.barh(candidats, apparition_positive, color='blue')
    negatif = plot.barh(candidats, apparition_negative, left=apparition_positive, color='orange')
    plot.legend([positif, negatif], ["Positif", "Total"], title="Avis", loc="upper right")
    plot.ylabel("Candidat")
    plot.xlabel("Tweets")
    # Save it to a temporary buffer.
    buf = io.BytesIO()
    figure = plot.gcf()
    figure.set_size_inches(12, 8)
    plot.savefig(buf, format="png", dpi=100)
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return render_template("index.html", title="Avis", img=f"{data}")


@app.route("/wordcloud")
def wordcloud():
    hists = os.listdir('static/img/candidats')
    hists = ['img/candidats/' + file for file in hists]
    return render_template('index.html', title="WordCloud", hists=hists)


@app.route("/search")
def search():
    return render_template('index.html', title="Search")


@app.route('/data_search', methods=['POST', 'GET'])
def data_from_search():
    global parti_user
    if request.method == 'POST':
        twitter_user = request.form['Twitter_user']
        scraping_user(twitter_user)
        create_model(preprocess=False, fit=False)
        predict_tweets_user(twitter_user)

        donnee = pd.read_csv(f"../scrapping/csv/users/{twitter_user}/df_final_{twitter_user}.csv", index_col=0)
        donnee = donnee.loc[donnee['candidat'] != 'None']

        candidats = donnee['candidat'].unique()

        candidats_gauche = ['arthaud', 'hidalgo', 'jadot', 'macron', 'mélenchon', 'poutou']
        candidats_droite = ['dupont-aignan', 'macron', 'pécresse', 'lasalle', 'le pen', 'zemmour']

        candidats = sorted(candidats, reverse=True)

        # gauche / droite
        apparition_positive_gauche = []
        apparition_negative_gauche = []

        apparition_positive_droite = []
        apparition_negative_droite = []

        for candidat in candidats:
            if candidat in candidats_droite:
                apparition_positive_droite.append(donnee.loc[donnee['candidat'] == candidat]['predicted'].sum())
                apparition_negative_droite.append((donnee.loc[donnee['candidat'] == candidat]['predicted'].count()) - (
                    donnee.loc[donnee['candidat'] == candidat]['predicted'].sum()))

            if candidat in candidats_gauche:
                apparition_positive_gauche.append(donnee.loc[donnee['candidat'] == candidat]['predicted'].sum())
                apparition_negative_gauche.append((donnee.loc[donnee['candidat'] == candidat]['predicted'].count()) - (
                    donnee.loc[donnee['candidat'] == candidat]['predicted'].sum()))

        print(apparition_positive_gauche)
        print(apparition_negative_gauche)
        print(apparition_positive_droite)
        print(apparition_negative_droite)

        if sum(apparition_positive_gauche) + sum(apparition_negative_gauche) != 0:

            result_gauche = sum(apparition_positive_gauche) * 100 / (
                        sum(apparition_positive_gauche) + sum(apparition_negative_gauche))
        else:
            result_gauche = 0

        if sum(apparition_positive_droite) + sum(apparition_positive_droite) != 0:

            result_droite = sum(apparition_positive_droite) * 100 / (
                    sum(apparition_positive_droite) + sum(apparition_positive_droite))
        else:
            result_droite = 0


        if result_gauche > result_droite:
            parti_user = 'gauche'
        if result_gauche < result_droite:
            parti_user = 'droite'
        if result_gauche == result_droite:
            parti_user = 'indefini'
            if result_gauche ==0 and result_droite == 0:
                return render_template('index.html', title='Search data', twitter_user=twitter_user,
                                       parti_user=parti_user,
                                       result_droite=result_droite, result_gauche=result_gauche)

        # wordcloud
        hists = os.listdir(f'static/img/users/{twitter_user}')
        hists = [f'img/users/{twitter_user}/' + file for file in hists]

        # avis
        plot = plt
        apparition_positive = []
        apparition_negative = []

        for candidat in candidats:
            apparition_positive.append(donnee.loc[donnee['candidat'] == candidat]['predicted'].sum())
            apparition_negative.append((donnee.loc[donnee['candidat'] == candidat]['predicted'].count()) - (
                donnee.loc[donnee['candidat'] == candidat]['predicted'].sum()))

        print(apparition_positive)
        print(apparition_negative)

        positif = plot.barh(candidats, apparition_positive, color='blue')
        negatif = plot.barh(candidats, apparition_negative, left=apparition_positive, color='orange')
        plot.legend([positif, negatif], ["Positif", "Total"], title="Avis", loc="upper right")
        plot.ylabel("Candidat")
        plot.xlabel("Tweets")
        # Save it to a temporary buffer.
        buf = io.BytesIO()
        figure = plot.gcf()
        figure.set_size_inches(12, 8)
        plot.savefig(buf, format="png", dpi=75)
        # Embed the result in the html output.
        data = base64.b64encode(buf.getbuffer()).decode("ascii")

        return render_template('index.html', title='Search data', twitter_user=twitter_user, parti_user=parti_user,
                               hists=hists, len_user=len(twitter_user) * 2 + 12, img=f"{data}", result_droite=result_droite, result_gauche=result_gauche)


def creation_graphique():
    graphique = Figure()
    return graphique


if __name__ == "__main__":
    app.run(debug=True)
