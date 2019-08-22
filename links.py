import json
import sys

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
            res['geocode'] = item['geocode']
            res['price'] = item['price']
            result['links'].append(res)
    return result

def jsonToHtml(jsonStr, blob_visning):
    # reload(sys)
    # sys.setdefaultencoding('utf-8')

    visnings = json.loads(blob_visning)

    tstr1 ="""<table>"""
    for item in jsonStr["links"]:

        #check if the link is present in the visnings.
        visning = {}
        for view in visnings['links']:
            if item['link'] in view['link']:
                visning = view['visnings']
                break

        map_link = "https://www.google.co.in/maps/place/"+item['address']
        tstr2 = """<tr>
            <th bgcolor="#2a3c3c" height="60" width="40%">
            <a href="{link}" style="color:#FFFFFF;" target="_blank">{text}</a>
            </th>
            <td height="40" bgcolor="#2a3c3c" style="padding-right: 25px;padding-left: 25px;">
            <font size="3" color="white">
            <a href="{map_link}" style="color:#FFFFFF;" target="_blank">{address}</a>, {area}, {price}
            </font>
            </td>
            <td>
            <table bgcolor="#2a3c3c">
            """.format(link=item['link'],
                       text=item['text'],
                       address=item['address'],
                       area=item['area'],
                       price=item['price'],
                       map_link=map_link)
        tstr1 += tstr2
        for date in visning:
            tstr3="""
            <tr>
            <td height="40"  width="300" style="padding-right: 25px;padding-left: 25px;"><font size="3" color="white">{date}</font></td>
            </tr>""".format(date=date)
            tstr1+=tstr3
        tstr4="""
        </table>
        </td>
        </tr>"""
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
        geoCode = item['geocode']
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