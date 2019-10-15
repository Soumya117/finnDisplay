import json
from helpers.JsonUtil import JsonUtil


def filter_json(json_str, input_data):
    result = {}
    result['links'] = []
    data = json.loads(json_str)
    for item in data['links']:
        time = item['time'].split('T')
        if input_data in time:
            res = {}
            JsonUtil(res, item).prepare_json(price=item['price'])
            result['links'].append(res)
    return result


def json_to_html(json_str, blob_visning):
    total = len(json_str['links'])
    visnings = json.loads(blob_visning)

    tstr1 = """<p><font size="5" color="white">Total: {total} </font></p>
    <table bgcolor="#2a3c3c" border="1px">""".format(total=total)
    for item in json_str["links"]:
        # check if the link is present in the visnings.
        visning = {}
        for view in visnings['links']:
            if item['link'] in view['link']:
                visning = view['visnings']
                break

        map_link = "https://www.google.co.in/maps/place/"+item['address']
        tstr2 = """<tr>
            <th  height="60" width="18%">
            <a href="{link}" style="color:#FFFFFF;" target="_blank">{text}</a>
            </th>
            <td height="40" width="15%" style="padding-right: 15px;padding-left: 15px;">
            <font size="3" color="white">
            <a href="{map_link}" style="color:#FFFFFF;" target="_blank">{address}</a>, {area}, {price}
            </font>
            </td>
            <td width="8%">
            <table height="40">
            """.format(link=item['link'],
                       text=item['text'],
                       address=item['address'],
                       area=item['area'],
                       price=item['price'],
                       map_link=map_link)
        tstr1 += tstr2
        for date in visning:
            tstr3 = """
            <tr>
            <td style="padding-right: 15px;padding-left: 15px;"><font size="3" color="white">{date}</font></td>
            </tr>""".format(date=date)
            tstr1 += tstr3
        tstr4 = """
        </table>
        </td>
        </tr>"""
        tstr1 += tstr4
    tstr6 = """</table>"""
    tstr1 += tstr6
    return tstr1


def create_gmap(json_str):
    result = {}
    result['markers'] = []
    result['info'] = []
    for item in json_str['links']:
        add = item['address']
        map_link = "https://www.google.co.in/maps/place/"+item['address']
        geo_code = item['geocode']
        info = """
        <div class="info_content" style="width:300px; margin: auto;">
        <h2>
        <a href="{link}" style="color:#000000;" target="_blank">{text}</a>
        </h2>
        <a href="{map_link}" style="color:#000000;" target="_blank">{address}</a>
        , {area}, {price}
        </div>""".format(address=add,
                         text=item['text'],
                         area=item['area'],
                         price=item['price'],
                         map_link=map_link,
                         link=item['link'])
        geo_code_address = []
        geo_code_address.append(item['address'])
        geo_code_address.append(geo_code['lat'])
        geo_code_address.append(geo_code['lng'])

        result['markers'].append(geo_code_address)
        result['info'].append(info)
    return result
