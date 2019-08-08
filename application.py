#!/usr/bin/env python
from azure.storage.blob import BlockBlobService, PublicAccess
from flask import jsonify
from flask import request
container_name ='finnblob'
from flask import Flask, render_template
app = Flask(__name__)
import json
import seaborn as sns
import io
import base64
import matplotlib.pyplot as plt
import multiplePris
import links
import sold
import visning
import sys

def readBlob(blobName):
    print("Reading blob: ", blobName)
    sys.stdout.flush()
    block_blob_service = BlockBlobService(account_name='accountName',
                                          account_key='AccountKey')
    blob = block_blob_service.get_blob_to_text(container_name, blobName)
    return blob.content

def readJson(jsonStr):
    dict = {}
    data = json.loads(jsonStr)
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
    plt.style.use('dark_background')
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

def graphLinks(jsonStr):
    dict_links = readJson(jsonStr)
    plot_url_links = prepareGraph(dict_links, 'Number of RealEstates Added', 'RealEstates')
    return plot_url_links

def graphSold(jsonStr):
    dict_sold = readJson(jsonStr)
    plot_url_sold = prepareGraph(dict_sold, 'Number of Houses Sold', 'Number of Houses Sold')
    return plot_url_sold

@app.route('/status', methods=['GET', 'POST'])
def finnData():
    filterDate = request.form['date']
    filterDate = filterDate.encode('ascii','ignore').decode('utf-8')

    print("Received date: ", filterDate)
    sys.stdout.flush()

    result = {}
    result['links'] = {}
    result['sold'] = {}
    result['price'] = {}
    result['visnings'] = {}

    blob_pris = readBlob('multiplePris.json')
    blob_links = readBlob('links.json')
    blob_sold = readBlob('sold.json')
    blob_visnings = readBlob('visning.json')

    filterLinks = links.filterJson(blob_links, filterDate)
    filterPrice = json.loads(blob_pris) #TODO Filter
    filterSold = sold.filterJson(blob_sold, filterDate)
    filterVisnings = json.loads(blob_visnings) #TODO Filter

    result['links']['table'] = links.jsonToHtml(filterLinks)
    result['links']['map'] = links.createGmap(filterLinks)

    result['price']['table'] = multiplePris.jsonToHtml(filterPrice)
    result['price']['map'] = multiplePris.createGmap(filterPrice)

    result['sold']['table'] = sold.jsonToHtml(filterSold)
    result['sold']['map'] = sold.createGmap(filterSold)

    result['visnings']['table'] = visning.jsonToHtml(filterVisnings)
    result['visnings']['map']= visning.createGmap(filterVisnings)

    return jsonify(result)

@app.route('/')
def renderGraph():
    blob_links = readBlob('links.json')
    blob_sold = readBlob('sold.json')
    return render_template("graph.html",
                  plot_url_links=graphLinks(blob_links),
                  plot_url_sold= graphSold(blob_sold))
