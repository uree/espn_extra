# -*- coding: utf-8 -*-
#python2.7

from bs4 import BeautifulSoup
from operator import itemgetter

filename = "League Standings - NBA prvakov - ESPN Fantasy Basketball.html"

def printout(rezultati):
    vrstica=''
    tabela=''

    for i in range(len(rezultati)):
        vrstica+=str(rezultati[i]['Team'])
        vrstica+=(37-len(vrstica))*' '

        for key in rezultati[i]:
            if key!='Team':
                try:
                    vrstica+=str(key)+':'+str(rezultati[i][key])+(10-len(str(rezultati[i][key])))*' '
                except TypeError:
                    print(key)
                    pass
        vrstica+='\n'
        tabela+=vrstica
        vrstica=''

    print(tabela)

def rejeni(slov):
    print("ROTISRI")
    rotis = []
    for i in range(len(slov)):
        one = {}
        tim = slov[i]['Team']
        one['Team'] = tim
        #print(tim)
        for key in slov[i]:
            if key != 'Team':
                vals = [n[key] for n in slov]
                if key == 'TO':
                    vals.sort(reverse=True)
                else:
                    vals.sort()
                #print("VALS", vals)
                val = slov[i][key]
                points = vals.index(val)+1
                one[key] = points
        total = sum([one[item] for item in one if item != 'Team'])
        one['TOTAL'] = total
        rotis.append(one)
    #print("ROTIS", rotis)
    sortd = sorted(rotis, key=itemgetter('TOTAL'), reverse=True)
    print("STD: ", sortd)
    return sortd


def obdelaj(podatki):
    sttekem=[]
    for i in range(len(podatki['teams'])):
        sttekem=sttekem+[int(podatki['teams'][i]['GP'])]
    normaliziraj=820

    #print(normaliziraj)

    #print sttekem

    rezultati=[]
    for i in range(len(podatki['teams'])):
        igralec=dict()
        igralec.update({'Team':podatki['teams'][i]['TEAM']})
        kategorije=['AST','STL','TO','3PM','BLK','REB','PTS']
        #print igralec
        for j in range(len(kategorije)):
            dat = podatki['teams'][i][kategorije[j]]
            gp = podatki['teams'][i]['GP']
            hem1 = int(dat)/float(int(gp))*820
            rhem = round(hem1)
            #print("dat:", dat, " gp:", gp, "hem1: ", hem1)
            #print(rhem)
            igralec.update({kategorije[j]:str(rhem)})

        rezultati=rezultati+[igralec]

    #print(rezultati)
    printout(rezultati)
    urejeni = rejeni(rezultati)
    printout(urejeni)


def formdict(table):
    base = {"teams": []}
    temp = []
    inner_tables = table.findAll('td', {"class": "v-top"})
    chcount = ''

    for table in inner_tables:
        chcount = 0
        hdrs = table.findAll('th')
        bhdrs = [h.text for h in hdrs if h.text != 'All' and h.text]
        data = table.findAll('td')
        bdata = [d.text for d in data if len(d.text) < 30 and d.text]

        step = len(bhdrs)
        rng = len(bdata)


        chunks = [bdata[x:x+step] for x in range(0, len(bdata), step)]
        #print(chunks)
        for chunk in chunks:
            chcount+=1
            op = {}
            for ch in range(len(chunk)):
                op[bhdrs[ch]] = chunk[ch]
            #print(op)
            temp.append(op)

        chcount = chcount

    start = 0
    while start < chcount:
        one = temp[start::chcount]
        done = {k.upper(): v for one in one for k, v in one.items()}
        #print(done)
        base['teams'].append(done)
        start+=1


    print(base)
    return(base)



def parsetable():
    html = open(filename,'r').read()

    soup = BeautifulSoup(html)
    #print(soup)
    stion = soup.select_one("#espn-analytics > div > div.jsx-813185768.shell-container > div.page-container.cf > div.layout.is-full > div > div > div.jsx-792047434.season--stats--table > section > table")

    data = formdict(stion)

    #print("\n\n""PROJEKCIJA"+"\n")

    obdelaj(data)




parsetable()
