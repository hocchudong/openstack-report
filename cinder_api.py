from common import get_api
from keystone_api import (get_token,get_endpoint,get_tenant_id,get_tenant_list)
import json
def get_volumes_list(tenant_id, token, hostname, cinder_port):
    method = 'GET'
    params = ''
    path = '/v2/'+tenant_id+'/volumes?all_tenants=1'
    header = {'Content-Type': 'application/json', 'X-Auth-Token': token}
    response = get_api(method, path, params, header, hostname, cinder_port)
    if response.status == 200:
        volumes = json.loads(response.read())
        return volumes
    if response.status == 400:
        error = 'Time out'
        return redirect(url_for('login', error=error))
if __name__ == '__main__':
    pass