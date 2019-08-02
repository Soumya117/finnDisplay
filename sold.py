import json

def jsonToHtml(jsonStr):
    tstr1 ="""
    <table>
    <thead bgcolor="#00001a">
    <tr>
    <th><font size="3" color="white">Ad</font></th>
    <td>
    <table>
    <tr>
    <th style="padding-right: 50x;padding-left: 50px;">
    <font size="3" color="white">Date</font></th>
    </tr>
    </table>
    </td>
    </tr>
    </thead>"""
    data = json.loads(jsonStr)
    for item in data["links"]:
        day = item['time'].split('T')
        tstr2 = """<tr>
        <th bgcolor="#2a3c3c" height="35">
        <a href="{link}" style="color:#FFFFFF;">{link}</a>
        </th>
        <td  height="35" bgcolor="#2a3c3c" style="padding-right: 25px;padding-left: 25px;"><font size="3" color="white">{time}</font></td>
        """.format(link=item['link'], time=day[0])
        tstr1 += tstr2
        tstr4="""</tr>"""
        tstr1+=tstr4
    tstr6="""</table>"""
    tstr1+=tstr6
    return tstr1
