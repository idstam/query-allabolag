import requests
from bs4 import BeautifulSoup
import json
import time



def getOmsattning(link):
    resp = requests.get("https://www.allabolag.se/%s" % link)
    if resp.status_code == 200:
        # print("Page %s" % pageNumber)
        html = resp.content
        soup = BeautifulSoup(html, 'html.parser')
        find_by_class = soup.find_all(class_='table--border-separator figures-table')
        if len(find_by_class) == 0:
            return '0'
        else:
            omsNod = soup.find_all(class_='number--positive')
            return omsNod[0].text.strip().replace(" ", "")

    return '0'

def search(theWord):
    doContinue = True
    pageNumber = 0
    doubleCheck = dict()
    f = open('d:\\temp\\allabolag.txt', 'a')

    while doContinue:
        pageNumber = pageNumber + 1
        resp = requests.get("https://www.allabolag.se/what/%s?page=%s" % (theWord, pageNumber))
        if resp.status_code == 200:
            # print("Page %s" % pageNumber)
            html = resp.content
            soup = BeautifulSoup(html, 'html.parser')
            find_by_class = soup.find_all('search')
            if len(find_by_class) == 0:
                break
            else:
                foo = find_by_class[0][':search-result-default']
                # print(foo)
                searchResults = json.loads(foo)
                # print(len(searchResults))
                print("__OrgNr\tNamn\tH-grupp\tU-grupp\tscore\tlink\tOmsattning")
                f.write("__OrgNr\tNamn\tH-grupp\tU-grupp\tscore\tlink\tOmsattning" + "\n")

                for result in searchResults:
                    if result['orgnr'] not in doubleCheck.keys():
                        doubleCheck[result['orgnr']] = result['jurnamn']
                        s = float(result['score']['0'])
                        if s < 70.0:
                            print("Getting low scores")
                            doContinue = False

                        #time.sleep(0.5)
                        oms = getOmsattning(result['linkTo'])

                        line = "%s\t%s\t%s\t%s\t%s\t%s\t%s" % (result['orgnr'], result['jurnamn'], result['abv_hgrupp'], result['abv_ugrupp'], result['score'], result['linkTo'], oms)
                        print(line)
                        f.write(line + "\n")
                    else:
                        print("Found double at page %s" % pageNumber)
                        doContinue = False
                        break
        else:
            break

        if pageNumber == 1000:
            break


# ordet = sys.argv[1]
ordet = 'bokföring'
search(ordet)
