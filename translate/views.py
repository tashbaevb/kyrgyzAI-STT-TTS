import json
import urllib.parse
import urllib.request


class Result:
    def __init__(self):
        self.data = None

    def __str__(self):
        return str(self.data)

    def unmarshal_json(self, data):
        try:
            v = json.loads(data)
            self.data = v[0][0][0]
        except Exception as e:
            print(e)
            return e


def translate_to_kyrg(from_lang: str, text: str):
    # from lang can be "ru" or "en"
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={from_lang}&tl=ky&dt=t&q=" + urllib.parse.quote(
        text)

    try:
        response = urllib.request.urlopen(url)
        bytes_data = response.read()
        result = Result()
        result.unmarshal_json(bytes_data)
        value = result.data
        return value
    except Exception as e:
        print(e)
        exit(1)


def translate_from_kyrg(to_lang: str, text: str):
    # to lang can be "ru" or "en"
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=ky&tl={to_lang}&dt=t&q=" + urllib.parse.quote(
        text)

    try:
        response = urllib.request.urlopen(url)
        bytes_data = response.read()
        result = Result()
        result.unmarshal_json(bytes_data)
        value = result.data
        return value
    except Exception as e:
        print(e)
        exit(1)
