import io
import os
import random
from flask import render_template, Response, Flask
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import base64
import pandas as pd

app = Flask(__name__)


@app.route('/')
def view_home():
    return render_template("index.html", title="Home")


@app.route("/avis")
def avis():
    plot = plt
    # Generate the figure **without using pyplot**.

    donnee = pd.read_csv("../nlp/csv/df_final.csv", index_col=0)
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
    hists = os.listdir('static/img')
    hists = ['img/' + file for file in hists]
    return render_template('index.html', title="WordCloud", hists=hists)


def creation_graphique():
    graphique = Figure()
    return graphique


if __name__ == "__main__":
    app.run(debug=True)
