import json
import sys
import markers

def filterJson(jsonStr, inputData):
    result = {}
    result['links'] = []
    data = json.loads(jsonStr)
    for item in data['links']:
        time = item['time'].split('T')
        if inputData in time:
            res = {}
            res['link'] = item['link']
            res['text'] = item['text']
            res['address'] = item['address']
            res['area'] = item['area']
            res['price'] = item['price']
            result['links'].append(res)
    return result

def jsonToHtml(jsonStr):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    tstr1 ="""<table>>"""
    for item in jsonStr["links"]:
        map_link = "https://www.google.co.in/maps/place/"+item['address']
        tstr2 = """<tr>
            <th bgcolor="#2a3c3c" height="40" width="40%">
            <a href="{link}" style="color:#FFFFFF;" target="_blank">{text}</a>
            </th>
            <td height="40" bgcolor="#2a3c3c" style="padding-right: 25px;padding-left: 25px;">
            <font size="3" color="white">
            <a href="{map_link}" style="color:#FFFFFF;" target="_blank">{address}</a>
            </font>
            </td>
            <td  height="40" bgcolor="#2a3c3c" style="padding-right: 25px;padding-left: 25px;"><font size="3" color="white">{price}</font></td>
            <td  height="40" bgcolor="#2a3c3c" style="padding-right: 25px;padding-left: 25px;"><font size="3" color="white">{area}</font></td>
            """.format(link=item['link'],
                       address=item['address'],
                       area=item['area'],
                       text=item['text'],
                       price=item['price'],
                       map_link=map_link)
        tstr1 += tstr2
        tstr4="""</tr>"""
        tstr1+=tstr4
    tstr6="""</table>"""
    tstr1+=tstr6
    return tstr1

def createGmap(jsonStr):
    result = {}
    result['markers'] = []
    result['info'] = []
    for item in jsonStr['links']:
        add = item['address']
        map_link = "https://www.google.co.in/maps/place/"+item['address']
        geoCode = markers.getMarkers(add)
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
        geoCodeAddress = []
        geoCodeAddress.append(item['address'])
        geoCodeAddress.append(geoCode['lat'])
        geoCodeAddress.append(geoCode['lng'])

        result['markers'].append(geoCodeAddress)
        result['info'].append(info)
    return result