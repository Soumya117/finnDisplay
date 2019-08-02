import json

def jsonToHtml():
    tstr1 ="""
    <html>
    <body>
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
    with open('multiplePris.json') as input:
        data = json.load(input)
        for link in data:
            tstr2 = """
            <tr>
            <th bgcolor="#e6e6e6" height="30">
            <a href="{link}">{link}</a>
            </th>
            <td>
            <table bgcolor="#e6e6e6">""".format(link=link)
            tstr1 += tstr2
            out = data[link]
            for pris in out:
                price = pris['pris']
                time = pris['time'].split('T')
                tstr3="""
                <tr>
                <td height="30" style="padding-right: 25px;padding-left: 25px;">{price}</td>
                <td height="30"style="padding-right: 25px;padding-left: 25px;">{time}</td>
                </tr>""".format(price=price, time=time[0])
                tstr1+=tstr3
            tstr4="""
            </table>
            </td>
            </tr>"""
            tstr1+=tstr4
    tstr6="""
    </table>
    </body>
    </html>"""
    tstr1+=tstr6
    print(tstr1)

