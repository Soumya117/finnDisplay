import json

def jsonToHtml():
    tstr1 ="""Content-type: text/html\n\n
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
    with open('sold.json') as input:
        data = json.load(input)
        for item in data["links"]:
            day = item['time'].split('T')
            tstr2 = """<tr>
            <th bgcolor="#e6e6e6"  height="35">
            <a href="{link}">{link}</a>
            </th>
            <td  height="35" bgcolor="#e6e6e6" style="padding-right: 25px;padding-left: 25px;">{time}</td>
            """.format(link=item['link'], time=day[0])
            tstr1 += tstr2
            tstr4="""</tr>"""
            tstr1+=tstr4
    tstr6="""</table>"""
    tstr1+=tstr6
    return tstr1

