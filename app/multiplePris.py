import json
from helpers.JsonUtil import JsonUtil


def filter_json(json_str, input_data):
    result = dict()
    result['links'] = []
    data = json.loads(json_str)
    for item in data['links']:
        time = item['time'].split('T')
        if input_data in time:
            res = dict()
            res['details'] = {}
            JsonUtil(res, item).prepare_json(data=item['details'], output=res['details'])
            res['price_list'] = item['price_list']
            result['links'].append(res)
    return result


def json_to_html(json_str, blob_visning, blob_sold):
    sold_houses = json.loads(blob_sold)
    visnings = json.loads(blob_visning)
    total = len(json_str['links'])
    tstr1 = """<p><font size="5" color="white">Total: {total} </font></p>
    <table bgcolor="#2a3c3c" border="1px">""".format(total=total)
    for item in json_str['links']:
        # check if the link is present in the visnings.
        visning = {}
        sold = {}
        sold['status'] = ""
        sold['time'] = ""
        for view in visnings['links']:
            if item['link'] in view['link']:
                visning = view['visnings']
                break
        for sold_item in sold_houses['links']:
            if item['link'] in sold_item['link']:
                sold['status'] = sold_item['status']
                sold['time'] = sold_item['time'].split('T')[0]
                break

        map_link = "https://www.google.co.in/maps/place/"+item['details']['address']
        tstr2 = """
        <tr>
        <th height="40" width="15%">
        <a href="{link}" style="color:#FFFFFF;" target="_blank">{text}</a>
        </th>
        <td height="40" width="15%" style="padding-right: 15px;padding-left:15px;">
        <font size="3" color="white">
        <a href="{map_link}" style="color:#FFFFFF;" target="_blank">{address}</a>, {area}
        </font>
        </td>
        <td height="40" width="9%">
        <table height="40">""".format(link=item['link'],
                                            address=item['details']['address'],
                                            text=item['details']['text'],
                                            area=item['details']['area'],
                                            map_link=map_link)
        tstr1 += tstr2
        out = item['price_list']
        for pris in out:
            price = pris['price']
            time = pris['time'].split('T')
            tstr3 = """
            <tr>
            <td style="padding-right: 15px;padding-left: 15px;"><font size="3" color="white">{price}</font></td>
            <td style="padding-right: 15px;padding-left: 15px;"><font size="3" color="white">{time}</font></td>
            </tr>""".format(price=price, time=time[0])
            tstr1 += tstr3
        tstr4 = """</table></td>"""
        tstr1 += tstr4
        tstr1 += """<td width="10%"><table height="40">"""
        for date in visning:
            tstr5 = """
            <tr>
            <td style="padding-right: 15px;padding-left: 15px;"><font size="3" color="white">{date}</font></td>
            </tr>""".format(date=date)
            tstr1 += tstr5
        tstr6 = """
        </table>
        </td>
        <td  width="9%" style="padding-right: 15px;padding-left: 15px;">
        <font size="3" color="white">{status}&nbsp;&nbsp;{time}
        </font></td>
        </tr>""".format(status=sold['status'], time=sold['time'])
        tstr1 += tstr6
    tstr7 = """
    </table>"""
    tstr1 += tstr7
    return tstr1


def create_gmap(json_str):
    result = {}
    result['markers'] = []
    result['info'] = []
    for item in json_str['links']:
        add = item['details']['address']
        map_link = "https://www.google.co.in/maps/place/"+item['details']['address']
        geo_code = item['details']['geocode']
        info = """
        <div class="info_content" style="width:300px; margin: auto;">
        <h2>
        <a href="{link}" style="color:#000000;" target="_blank">{text}</a>
        </h2>
        <a href="{map_link}" style="color:#000000;" target="_blank">{address}</a>
        , {area}
        </div>""".format(address=add,
                         text=item['details']['text'],
                         area=item['details']['area'],
                         map_link=map_link,
                         link=item['link'])
        geo_code_address = []
        geo_code_address.append(item['details']['address'])
        geo_code_address.append(geo_code['lat'])
        geo_code_address.append(geo_code['lng'])

        result['markers'].append(geo_code_address)
        result['info'].append(info)
    return result
