import requests

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

