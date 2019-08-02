#!/usr/bin/env python
import os, uuid, sys
from azure.storage.blob import BlockBlobService, PublicAccess

container_name ='finnblob'

from flask import Flask, render_template
app = Flask(__name__)
import json
import seaborn as sns
import sys
import io
import base64
import matplotlib.pyplot as plt
import multiplePris
import links
import sold
import tabs

def readBlob(blobName):
    block_blob_service = BlockBlobService(account_name='finnminingblob', account_key='B3GcfOYBEci9aLYSFo6+KZpahLM52FlMGpFOvK/sD7HbeYspxCCCcAJG0ffnaXlmn8YfgSEarzrCyg5bIRN5Fg==')
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

@app.route('/')
def renderGraph():
    blob_pris = readBlob('multiplePris.json')
    blob_links = readBlob('links.json')
    blob_sold = readBlob('sold.json')
    realestates = links.jsonToHtml(blob_links)
    prices = multiplePris.jsonToHtml(blob_pris)
    soldHouses = sold.jsonToHtml(blob_sold)
    tabs1 = tabs.jsonToHtml()
    tabs1 = tabs1.format(
                  realestates=realestates,
                  price=prices,
                  soldHouses=soldHouses,
                  plot_url_links=graphLinks(blob_links),
                  plot_url_sold= graphSold(blob_sold))
    return tabs1
