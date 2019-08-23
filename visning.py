import json
import sys
import datetime

def parseDate(dateStr, inputDate):
    #prepare proper date from the visning dates
    date = dateStr.split(", ")[0]
    day = date.split(" ")
    now = datetime.datetime.now()
    tmpDate = day[1].strip('.') + " " + day[2] + " " +  str(now.year)
    finalDate = datetime.datetime.strptime(tmpDate, '%d %B %Y').strftime('%Y-%m-%d')

    if inputDate == finalDate:
        return True

def filterJson(jsonStr, filterDate):
    result = {}
    result['links'] = []
    data = json.loads(jsonStr)
    for item in data['links']:
        upcoming = False
        for date in item['visnings']:
            if parseDate(date, filterDate):
                upcoming = True
                break
        if upcoming:
            res = {}
            res['link'] = item['link']
            res['details'] = {}
            res['details']['text'] = item['details']['text']
            res['details']['address'] = item['details']['address']
            res['details']['geocode'] = item['details']['geocode']
            res['details']['area'] = item['details']['area']
            res['details']['price'] = item['details']['price']
            res['visnings'] = item['visnings']
            result['links'].append(res)
    return result

def jsonToHtml(jsonStr):
    # reload(sys)
    # sys.setdefaultencoding('utf-8')
    total = len(jsonStr['links'])
    tstr1 ="""<p><font size="5" color="white">Total: {total} </font></p>
    <table>""".format(total=total)
    for item in jsonStr['links']:
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
    tstr6="""
    </table>"""
    tstr1+=tstr6
    return tstr1

def createGmap(jsonStr):
    result = {}
    result['markers'] = []
    result['info'] = []
    for item in jsonStr['links']:
        add = item['details']['address']
        map_link = "https://www.google.co.in/maps/place/"+item['details']['address']
        geoCode = item['details']['geocode']
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
        geoCodeAddress = []
        geoCodeAddress.append(item['details']['address'])
        geoCodeAddress.append(geoCode['lat'])
        geoCodeAddress.append(geoCode['lng'])

        result['markers'].append(geoCodeAddress)
        result['info'].append(info)
    return result