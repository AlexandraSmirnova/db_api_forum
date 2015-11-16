__author__ = 'AS'
import urlparse

def check_data(data, required):
    for el in required:
        if el not in data:
            raise Exception("required element " + el + " not in parameters")
        if data[el] is not None:
            try:
                data[el] = data[el].encode('utf-8')               
            except Exception:
                continue
    print("Data is OK!")
    return


def intersection(request, values):
    optional = dict([(k, request[k]) for k in set(values) if k in request])
    return optional


def get_json(request):
    if request.method == 'GET':
        return dict((k, v if len(v) > 1 else v[0] )
                    for k, v in urlparse.parse_qs(request.query_string).iteritems())
    else:
        return request.json

    
def related_exists(request):
    try:
        related = request["related"]
    except Exception:
        related = []
    return related