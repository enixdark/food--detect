import requests

def translate(query):
    r = requests.post(
        'https://translation.googleapis.com/language/translate/v2?key=AIzaSyA_pAq4hN25gKOTCsJN-Z4aY8dEMZjvhyU '
        , json={
            'q': query,
            'target': 'en'
        })
    result = r.json()
    return result

if __name__ == '__main__':
    translate("Thịt ba chỉ: 500g\
– Thịt nạc vai: 500g")
