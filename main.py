import urllib.request
import json
import requests
import time

DEBUG = True


def setup_url():
    # change content type to json
    return urllib.request.urlopen('https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/Document?$top=100')


def be_nice_to_the_server():
    # be nice to the server and sleep for a while
    if DEBUG:
        pass
    else:
        time.sleep(5)


def main():
    contents = setup_url()
    x = json.loads(contents.read().decode('utf-8'))
    if DEBUG:
        print('DEBUG: main()')
        for i in range(len(x['value'])):
            be_nice_to_the_server()
            print(x['value'][i]['Id'], i)
    else:
        # for i in range(len(x['value'])):
        for i in range(5):
            be_nice_to_the_server()
            if x['value'][i]['DocumentNummer'] is not None and x['value'][i]['ContentLength'] is not None:
                r = requests.get(
                    'https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/document/' + x['value'][i]['Id'] + '/resource')

                if r.status_code == 200 and r.headers['Content-Type'] == 'application/pdf':
                    with open('download/' + x['value'][i]['Id'] + '.pdf', 'wb') as f:
                        f.write(r.content)
                elif r.status_code == 200 and r.headers['Content-Type'] == 'application/msword':
                    with open('download/' + x['value'][i]['Id'] + '.doc', 'wb') as f:
                        f.write(r.content)
                elif r.status_code == 200 and r.headers['Content-Type'] == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                    with open('download/' + x['value'][i]['Id'] + '.docx', 'wb') as f:
                        f.write(r.content)
                else:
                    # skip this document
                    pass


if __name__ == '__main__':
    main()
