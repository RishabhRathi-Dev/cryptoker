
from bs4 import BeautifulSoup
import  lxml
import requests

def LanguageData(userName):

    """
    This function take a string userName as input which is then used to find the users repositories and scrap data from repository page.

    """

    usrName = userName
    page = 1

    URL = f"https://github.com/{usrName}?tab=repositories"

    totals = 0
    langDict = {}

    def addLanguage(language):
        try:
            langDict[language] += 1
        except KeyError:
            langDict[language] = 1
        

    while True:
        
        my_userPage = requests.get(URL).text

        soup = BeautifulSoup(my_userPage, 'lxml')
        public = soup.find_all('li', class_ = "col-12 d-flex flex-justify-between width-full py-4 border-bottom color-border-muted public source")

        if len(public) < 1:
            break

        for pub in public:
            try:
                languages = pub.find('span', itemprop="programmingLanguage").text
                addLanguage(languages)
                totals += 1

            except AttributeError:
                print("No Languages for this repository")

            

        page += 1

        URL = f"https://github.com/{usrName}?page={page}&tab=repositories"

        

    print(langDict)
    print(totals)

    return langDict, totals

