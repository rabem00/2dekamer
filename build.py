from importlib.resources import contents
import urllib.request
import json
import requests
import time
import uuid
import pandas as pd

num_docs = 100

features = [
    "Id",
    "Soort",
    "DocumentNummer",
    "Onderwerp",
    "Datum",
    "ContentLength",
    "ContentType",
    "Organisatie"
]


def be_nice_to_remote():
    # be nice to the server and sleep for a while
    time.sleep(1)


def main():
    # Creating a DF for these features
    df = pd.DataFrame(columns=features)

    # Get first page of documents (250 documents per page)
    contents = urllib.request.urlopen(
        'https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/Document?$top=250')
    x = json.loads(contents.read().decode('utf-8'))

    for i in range(len(x['value'])):
        be_nice_to_remote()
        if x['value'][i]['DocumentNummer'] is not None and x['value'][i]['ContentLength'] is not None and x['value'][i]['ContentType'] == 'application/pdf':
            r = requests.get(
                'https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/document/' + x['value'][i]['Id'] + '/resource')

            # Save the document to a file
            with open('download/' + x['value'][i]['Id'] + '.pdf', 'wb') as f:
                f.write(r.content)

            # Add the document to the DF
            df.loc[i] = [
                x['value'][i]['Id'],
                x['value'][i]['Soort'],
                x['value'][i]['DocumentNummer'],
                x['value'][i]['Onderwerp'],
                x['value'][i]['Datum'],
                x['value'][i]['ContentLength'],
                x['value'][i]['ContentType'],
                x['value'][i]['Organisatie']
            ]

    # Save the DF to a CSV file
    df.to_csv('dataset.csv')

    # Read the CSV file
    # pd.read_csv('dataset.csv', index_col=0)


if __name__ == '__main__':
    main()
