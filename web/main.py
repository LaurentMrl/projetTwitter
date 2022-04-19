import io
import random
from flask import render_template, Response, Flask
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import base64
import pandas as pd

app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template("index.html")

@app.route('/plot.png')
def plot_png():
    graphique = creation_graphique()
    sortie = io.BytesIO()
    FigureCanvas(graphique).print_png(sortie)
    return Response(sortie.getvalue(), mimetype='image/png')

@app.route("/")
def hello():
    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()
    ax.plot([1, 2])
    # Save it to a temporary buffer.
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"

@app.route("/a")
def nono():
    plot = plt
    # Generate the figure **without using pyplot**.
    candidats = ["zemmour", "macron", "pécresse", "mélenchon", "jadot", "dupont-aignan", "arthaud", "hidalgo", "poutou",
                 "le pen", "roussel", "lassalle"]

    candidats = sorted(candidats, reverse=True)

    donnee = pd.read_csv("../nlp/csv/df_final.csv", index_col=0)

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
    # Save it to a temporary buffer.
    buf = io.BytesIO()
    plot.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"

def creation_graphique():
    graphique = Figure()
    return graphique

if __name__ == "__main__":
    app.run(debug=True)