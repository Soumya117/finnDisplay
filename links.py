import json

def jsonToHtml(jsonStr, inputDate):
    tstr1 ="""<table>"""
    data = json.loads(jsonStr)
    for item in data["links"]:
        day = item['time'].split('T')
        if inputDate in day:
            tstr2 = """<tr>
            <th bgcolor="#2a3c3c" height="60" width="40%">
            <a href="{link}" style="color:#FFFFFF;">{text}</a>
            </th>
            <td height="40" bgcolor="#2a3c3c" style="padding-right: 25px;padding-left: 25px;"><font size="3" color="white">{address}</font></td>
            <td height="40" bgcolor="#2a3c3c" style="padding-right: 25px;padding-left: 25px;"><font size="3" color="white">{area}</font></td>
            <td height="40" bgcolor="#2a3c3c" style="padding-right: 25px;padding-left: 25px;"><font size="3" color="white">{price}</font></td>
            """.format(link=item['link'],
                       text=item['text'],
                       address=item['address'],
                       area=item['area'],
                       price=item['price'])
            tstr1 += tstr2
            tstr4="""</tr>"""
            tstr1+=tstr4
    tstr6="""</table>"""
    tstr1+=tstr6
    return tstr1
