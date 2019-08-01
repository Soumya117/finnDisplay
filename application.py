from flask import Flask, render_template
app = Flask(__name__)
import json
import seaborn as sns
import io
import base64
import matplotlib.pyplot as plt

def readJson(file):
    dict = {}
    with open(file) as input:
        data = json.load(input)
        for item in data["links"]:
            time = item['time'].split('T')
            day = time[0]
            if day in dict:
                dict[day] += 1
            else:
                dict[day] = 1
    return dict

def prepareGraph(dict, yLabel, title):
    img = io.BytesIO()
    sns.set_style("dark") #E.G.
    x = []
    y = []
    for k in sorted(dict):
        x.append(k)
        y.append(dict[k])
    plt.plot(x,y)
    plt.legend(loc='upper left',prop = {'size':7},bbox_to_anchor=(1,1))
    plt.tight_layout(pad=5)
    plt.ylabel(yLabel)
    plt.title(title)
    plt.grid()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    return plot_url

def graphLinks():
    dict_links = readJson("links_Week.json")
    plot_url_links = prepareGraph(dict_links, 'Number of RealEstates Added', 'RealEstates')
    return plot_url_links

def graphSold():
    dict_sold = readJson("sold.json")
    plot_url_sold = prepareGraph(dict_sold, 'Number of Houses Sold', 'Number of Houses Sold')
    return plot_url_sold

@app.route('/')
def renderGraph():
    return render_template('graph.html',
                           plot_url_links=graphLinks(),
                           plot_url_sold=graphSold())