import json
import sys

def jsonToHtml(jsonStr, inputDate):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    tstr1 ="""<table>>"""
    data = json.loads(jsonStr)
    for item in data["links"]:
        day = item['time'].split('T')
        map_link = "https://www.google.co.in/maps/place/"+item['address']
        if inputDate in day:
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
