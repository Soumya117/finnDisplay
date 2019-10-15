import json
import datetime
from helpers.JsonUtil import JsonUtil


def parse_date(date_str, input_date):
    # prepare proper date from the visning dates
    months = {
        "januar": 1,
        "februar": 2,
        "mars": 3,
        "april": 4,
        "mai": 5,
        "juni": 6,
        "juli": 7,
        "august": 8,
        "september": 9,
        "oktober": 10,
        "november": 11,
        "desember": 12
    }

    date = date_str.split(", ")[0]
    day = date.split(" ")
    now = datetime.datetime.now()
    month = str(months[day[2]])
    tmp_date = day[1].strip('.') + " " + month + " " + str(now.year)
    final_date = datetime.datetime.strptime(tmp_date, '%d %m %Y').strftime('%Y-%m-%d')

    if input_date == final_date:
        return True


def filter_json(json_str, filter_date):
    result = {}
    result['links'] = []
    data = json.loads(json_str)
    for item in data['links']:
        upcoming = False
        for date in item['visnings']:
            if parse_date(date, filter_date):
                upcoming = True
                break
        if upcoming:
            res = {}
            res['details'] = {}
            JsonUtil(res, item).prepare_json(data=item['details'], output=res['details'])
            res['details']['price'] = item['details']['price']
            res['visnings'] = item['visnings']
            result['links'].append(res)
    return result


def json_to_html(json_str):
    total = len(json_str['links'])
    tstr1 = """<p><font size="5" color="white">Total: {total} </font></p>
    <table>""".format(total=total)
    for item in json_str['links']:
        map_link = "https://www.google.co.in/maps/place/"+item['details']['address']
        tstr2 = """
        <tr>
        <th bgcolor="#2a3c3c" height="40" width="40%">
        <a href="{link}" style="color:#FFFFFF;" target="_blank">{text}</a>
        </th>
        <td height="40" bgcolor="#2a3c3c" style="padding-right: 25px;padding-left: 25px;">
        <font size="3" color="white">
        <a href="{map_link}" style="color:#FFFFFF;" target="_blank">{address}</a>
        </font>
        </td>
        <td height="40" width="100" bgcolor="#2a3c3c" style="padding-right: 25px;padding-left: 25px;"><font size="3" color="white">{area}</font></td>
        <td height="40" width="150" bgcolor="#2a3c3c" style="padding-right: 25px;padding-left: 25px;"><font size="3" color="white">{price}</font></td>
        <td>
        <table bgcolor="#2a3c3c">""".format(link=item['link'],
                                            address=item['details']['address'],
                                            text=item['details']['text'],
                                            area=item['details']['area'],
                                            price=item['details']['price'],
                                            map_link=map_link)
        tstr1 += tstr2
        out = item['visnings']
        for date in out:
            tstr3 = """
            <tr>
            <td height="40"  width="300" style="padding-right: 25px;padding-left: 25px;"><font size="3" color="white">{date}</font></td>
            </tr>""".format(date=date)
            tstr1 += tstr3
        tstr4 = """
            </table>
            </td>
            </tr>"""
        tstr1 += tstr4
    tstr6 = """
    </table>"""
    tstr1 += tstr6
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
        , {area}, {price}
        </div>""".format(address=add,
                         text=item['details']['text'],
                         area=item['details']['area'],
                         price=item['details']['price'],
                         map_link=map_link,
                         link=item['link'])
        geo_code_address = []
        geo_code_address.append(item['details']['address'])
        geo_code_address.append(geo_code['lat'])
        geo_code_address.append(geo_code['lng'])

        result['markers'].append(geo_code_address)
        result['info'].append(info)
    return result
