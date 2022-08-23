from urllib import response
import requests
import json
import os
import shutil


def afficher_erreur_api(erreur):
    """Affiche les erreurs soulevées lors de l'interrogation de l'API HAL
    Paramètre = erreur"""
    "Les résultats HAL n'ont pas pu être récupérés ({erreur})."
    exit()

api_prefix = 'http://api.archives-ouvertes.fr/search/?q=authIdHal_s:mathieu-leonardon'

names = ['full', 'journal', 'conference', 'poster']
requetes = [api_prefix +"&wt=bibtex&sort=producedDateY_i desc",
            api_prefix +"&fq=docType_s:ART&wt=bibtex&sort=producedDateY_i desc",
            api_prefix +"&fq=docType_s:COMM&wt=bibtex&sort=producedDateY_i desc",
            api_prefix +"&fq=docType_s:POSTER&wt=bibtex&sort=producedDateY_i desc"]
reponses = []


if __name__ == '__main__':
    try:
        for requete in requetes:
            reponse = requests.get(requete, timeout=5)
            reponse = reponse.text
            reponse = reponse.replace("Leonardon","L{\\'e}onardon")
            reponse = reponse.replace("L{\\'e}onardon, Mathieu", "\\textbf{L{\\'e}onardon, Mathieu}")
            
            reponses.append(reponse)
            

    except requests.exceptions.HTTPError as errh:
        afficher_erreur_api(errh)
    except requests.exceptions.ConnectionError as errc:
        afficher_erreur_api(errc)
    except requests.exceptions.Timeout as errt:
        afficher_erreur_api(errt)
    except requests.exceptions.RequestException as err:
        afficher_erreur_api(err)
    

    dictionary = dict(zip(names,reponses))
    for name in dictionary:
        with open(name + '.bib', 'w') as file:
            file.write(dictionary[name])

fields="fl=abstract_s,docid,label_s,title_s, producedDate_tdate,uri_s,"
fields+="journalTitle_s,conferenceTitle_s,journalPublisher_s,doiId_s,docType_s,"
fields+="authLastName_s,producedDateY_i,authFullName_s,keyword_s,fileMain_s"

requete_json = api_prefix +"&wt=json&"+fields+"&sort=producedDateY_i desc"


if __name__ == '__main__':
    try:
        reponse = requests.get(requete_json, timeout=5).json()

    except requests.exceptions.HTTPError as errh:
        afficher_erreur_api(errh)
    except requests.exceptions.ConnectionError as errc:
        afficher_erreur_api(errc)
    except requests.exceptions.Timeout as errt:
        afficher_erreur_api(errt)
    except requests.exceptions.RequestException as err:
        afficher_erreur_api(err)
    

    # dump jsons in files
    with open('full.json', 'w') as file:
        json.dump(reponse, file, indent=2, ensure_ascii=False)

    path = './website/publication/'
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

    with open('./featured.txt','r') as f:
        featured_pubs = f.readlines()

    pubtype_dict = {"THESE" : "7", "ART" : "2", "COMM" : "1"}

    for pub in reponse['response']['docs']:
        if pub['docType_s'] not in pubtype_dict.keys():
            continue
        dirname = str(pub['producedDateY_i'])
        dirname += '-'
        dirname += ''.join(e for e in pub['authLastName_s'][0] if e.isalnum())
        dirname += '-'
        dirname += pub['docid']
        dirname += '/'
        os.makedirs(path + dirname)
        if os.path.exists('./pictures/' + str(pub['docid']) + '.png'):
            shutil.copyfile('./pictures/' + str(pub['docid']) + '.png', path + dirname + 'featured.png')
        with open(path + dirname + 'index.md', 'w') as f:
            f.write('+++\n')
            f.write('title = \"' + pub['title_s'][0]+ '\"\n')
            f.write('date = ' + pub['producedDate_tdate']+ '\n')
            f.write('authors = ' + str(pub['authFullName_s'])+ '\n')
            f.write('publication_types = [\"' + pubtype_dict[pub['docType_s']]+ '\"]\n')
            f.write('abstract = \"' + pub['abstract_s'][0].replace('\"','\'')+ '\"\n')
            featured = False
            for line in featured_pubs:
                if pub['docid'] in line:
                    featured = True
            if featured:
                f.write('featured = true\n')
            else:
                f.write('featured = false\n')
            if pub['docType_s'] == "ART":
                f.write('publication = \"' + pub['journalTitle_s'] + ' (' + pub['journalPublisher_s'] +')\"\n')
            elif pub['docType_s'] == "COMM":
                f.write('publication = \"' + pub['conferenceTitle_s'] + '\"\n')
            if 'keyword_s' in pub.keys():
                f.write('tags = ' + str(pub['keyword_s']) + '\n')
            if 'doiId_s' in pub.keys():
                f.write('doi = \"' + pub['doiId_s'] + '\"\n')
            if 'fileMain_s' in pub.keys():
                f.write('url_pdf = \"' + pub['fileMain_s'] + "\"\n")
            f.write('+++\n')




