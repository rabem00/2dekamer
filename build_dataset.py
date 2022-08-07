from importlib.resources import contents
from itertools import count
import urllib.request
import json
import requests
import time
import uuid
import pandas as pd

# Number of documents to download
num_docs = 5

# https://opendata.tweedekamer.nl/documentatie/document for the "Soort" column
download_soort = 'Motie'

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
    # be nice to the remote server and sleep for a while
    time.sleep(2)


def main():
    # Creating a DF for these features
    df = pd.DataFrame(columns=features)

    # Get first page of documents (250 documents per page)
    contents = urllib.request.urlopen(
        'https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/Document?$top=250')
    x = json.loads(contents.read().decode('utf-8'))

    count = 0
    for i in range(len(x['value'])):
        # be_nice_to_remote()
        if x['value'][i]['DocumentNummer'] is not None and x['value'][i]['ContentLength'] is not None and x['value'][i]['ContentType'] == 'application/pdf' and x['value'][i]['Soort'] == download_soort:
            r = requests.get(
                'https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/document/' + x['value'][i]['Id'] + '/resource')

            # Save the document to a file
            with open('download/' + x['value'][i]['Id'] + '.pdf', 'wb') as f:
                f.write(r.content)

            # Add the document to the DF
            df.loc[count] = [
                x['value'][i]['Id'],
                x['value'][i]['Soort'],
                x['value'][i]['DocumentNummer'],
                x['value'][i]['Onderwerp'],
                x['value'][i]['Datum'],
                x['value'][i]['ContentLength'],
                x['value'][i]['ContentType'],
                x['value'][i]['Organisatie']
            ]
            count += 1
            # Stop if we have enough documents
            if count == num_docs:
                break

    # Save the DF to a CSV file
    df.to_csv('dataset.csv')

    # Read the CSV file
    docs = pd.read_csv('dataset.csv', index_col=0)
    docs.head()


if __name__ == '__main__':
    main()
