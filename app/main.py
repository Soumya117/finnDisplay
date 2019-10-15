#!/usr/bin/env python
from azure.storage.blob import BlockBlobService, PublicAccess
from flask import jsonify
from flask import request
from flask import Flask, render_template
import json
import io
import base64
import matplotlib.pyplot as plt
import multiplePris
import links
import sold
import visning
from datetime import datetime
from logger import log

app = Flask(__name__)


def read_blob(blob_name):
    log("Reading blob: {}".format(blob_name))
    container_name = 'finnblob'
    block_blob_service = BlockBlobService(account_name='account_name',
                                          account_key='account_key')
    blob = block_blob_service.get_blob_to_text(container_name, blob_name)
    return blob.content


def prepare_date(date_str):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    day = date.strftime("%d")
    month = date.strftime("%B")
    result = day + " " + month
    return result


def read_json(json_str):
    result = {}
    data = json.loads(json_str)
    for item in data["links"]:
        time = item['time'].split('T')
        day = time[0]
        if day in result:
            result[day] += 1
        else:
            result[day] = 1
    return result


def prepare_graph(result, yLabel, title):
    img = io.BytesIO()
    plt.switch_backend('SVG')
    x = []
    y = []
    font = {'size': 25}
    plt.rc('font', **font)
    dict_size = len(result)
    if len(result) > 10:
        dict_size = 10
    for k in sorted(result)[len(result)-dict_size:len(result)]:
        x.append(k)
        y.append(result[k])
    plt.style.use('dark_background')
    plt.plot(x,y, color="r")
    plt.gcf().set_size_inches(30, 13)
    plt.legend(loc='upper left', prop={'size': 25}, bbox_to_anchor=(1, 1))
    plt.tight_layout(pad=5)
    plt.ylabel(yLabel)
    plt.title(title)
    plt.grid(linestyle='-', linewidth='2')
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    return plot_url


def graph_links(json_str):
    dict_links = read_json(json_str)
    plot_url_links = prepare_graph(dict_links, 'Number of RealEstates Added', 'RealEstates')
    return plot_url_links


def graph_sold(json_str):
    dict_sold = read_json(json_str)
    plot_url_sold = prepare_graph(dict_sold, 'Number of Houses Sold', 'Sold Status')
    return plot_url_sold


def receive_date():
    filter_date = request.form['date']
    filter_date = filter_date.encode('ascii', 'ignore').decode('utf-8')
    log("Received date: {}".format(filter_date))
    return filter_date


@app.route('/status/visnings', methods=['GET', 'POST'])
def get_visnings():
    filter_date = receive_date()

    result = dict()
    result['visnings'] = {}

    blob_visnings = read_blob('visning.json')

    log("Filtering jsons..!!")

    filter_visnings = visning.filter_json(blob_visnings, filter_date)

    result['visnings']['table'] = visning.json_to_html(filter_visnings)
    result['visnings']['map'] = visning.create_gmap(filter_visnings)

    log("Returning data...")

    return jsonify(result)


@app.route('/status/sold', methods=['GET', 'POST'])
def get_sold():
    filter_date = receive_date()

    result = dict()
    result['sold'] = {}

    blob_sold = read_blob('sold.json')
    blob_visnings = read_blob('visning.json')

    log("Filtering jsons..!!")

    filter_sold = sold.filter_json(blob_sold, filter_date)

    result['sold']['table'] = sold.json_to_html(filter_sold, blob_visnings)
    result['sold']['map'] = sold.create_gmap(filter_sold)

    log("Returning data...")

    return jsonify(result)


@app.route('/status/price', methods=['GET', 'POST'])
def get_price():
    result = dict()
    result['price'] = {}

    blob_pris = read_blob('multiplePris.json')
    blob_visnings = read_blob('visning.json')
    blob_sold = read_blob('sold.json')

    log("Filtering jsons..!!")

    filter_price = json.loads(blob_pris)

    result['price']['table'] = multiplePris.json_to_html(filter_price, blob_visnings, blob_sold)
    result['price']['map'] = multiplePris.create_gmap(filter_price)

    log("Returning data...")

    return jsonify(result)


@app.route('/status/realestates', methods=['GET', 'POST'])
def get_realestates():
    filter_date = receive_date()

    result = dict()
    result['realestates'] = {}

    blob_links = read_blob('links.json')
    blob_visnings = read_blob('visning.json')

    log("Filtering jsons..!!")

    filter_links = links.filter_json(blob_links, filter_date)

    result['realestates']['table'] = links.json_to_html(filter_links, blob_visnings)
    result['realestates']['map'] = links.create_gmap(filter_links)

    log("Returning data...")

    return jsonify(result)


@app.route('/')
def render_graph():
    blob_links = read_blob('links.json')
    blob_sold = read_blob('sold.json')
    return render_template("graph.html",
                           plot_url_links=graph_links(blob_links),
                           plot_url_sold= graph_sold(blob_sold))
