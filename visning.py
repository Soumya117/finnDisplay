import json

def jsonToHtml(jsonStr, inputDate):
    tstr1 ="""<table>"""
    data = json.loads(jsonStr)
    for item in data['links']:
        tstr2 = """
        <tr>
        <th bgcolor="#2a3c3c" height="40" width="40%">
        <a href="{link}" style="color:#FFFFFF;">{text}</a>
        </th>
        <td height="40" width="20%" bgcolor="#2a3c3c" style="padding-right: 25px;padding-left: 25px;"><font size="3" color="white">{address}</font></td>
        <td height="40" width="100" bgcolor="#2a3c3c" style="padding-right: 25px;padding-left: 25px;"><font size="3" color="white">{area}</font></td>
        <td height="40" width="150" bgcolor="#2a3c3c" style="padding-right: 25px;padding-left: 25px;"><font size="3" color="white">{price}</font></td>
        <td>
        <table bgcolor="#2a3c3c">""".format(link=item['link'],
                                            address=item['details']['address'],
                                            text=item['details']['text'],
                                            area=item['details']['area'],
                                            price=item['details']['price'])
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