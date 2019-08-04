import json

def jsonToHtml(jsonStr, inputDate):
    tstr1 ="""
    <table>
    <thead bgcolor="#00001a">
    <tr>
    <th><font size="3" color="white">Ad</font></th>
    <td>
    <table>
    <tr>
    <th style="padding-right: 50x;padding-left: 50px;">
    <font size="3" color="white">Price</font></th>
    <th style="padding-right: 60px;padding-left: 60px;">
    <font size="3" color="white">&nbsp&nbsp&nbsp&nbspDate</font></th>
    </tr>
    </table>
    </td>
    </tr>
    </thead>"""
    data = json.loads(jsonStr)
    for link in data:
        tstr2 = """
        <tr>
        <th bgcolor="#2a3c3c" height="30">
        <a href="{link}" style="color:#FFFFFF;">{link}</a>
        </th>
        <td>
        <table bgcolor="#2a3c3c">""".format(link=link)
        tstr1 += tstr2
        out = data[link]
        for pris in out:
            price = pris['pris']
            time = pris['time'].split('T')
            tstr3="""
            <tr>
            <td height="30" style="padding-right: 25px;padding-left: 25px;"><font size="3" color="white">{price}</font></td>
            <td height="30"style="padding-right: 25px;padding-left: 25px;"><font size="3" color="white">{time}</font></td>
            </tr>""".format(price=price, time=time[0])
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
