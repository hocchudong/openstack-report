import httplib


# connect restful API
def get_api(method, path, params, header, hostname, port):
    # print hostname
    conn = httplib.HTTPConnection(hostname, int(port))
    conn.request(method, path, params, header)
    resp = conn.getresponse()
    return resp


if __name__ == '__main__':
    pass
