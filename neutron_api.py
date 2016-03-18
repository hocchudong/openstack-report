import json

from neutronclient.common import exceptions as neutron_exc
from neutronclient.neutron import client as neutron_client

from common import get_api
from keystone_api import (get_endpoint)


# check neutron service
def check_neutron_service(token, tenant_id, hostname, keystone_port, username, password):
    neutron_endpoint = get_endpoint('admin', 'neutron', username, password, hostname, keystone_port)
    try:
        neutron = neutron_client.Client('2.0', token=token, endpoint_url=neutron_endpoint)
    except neutron_exc.NeutronClientException as e:
        error = str(e)
    agents = neutron.list_agents()
    agents = agents['agents']
    return agents

# get all port are using 

def get_ports(token, hostname, neutron_port):
    method = 'GET'
    params = ''
    path = '/v2.0/ports'
    header = {'Content-Type': 'application/json', 'X-Auth-Token': token}
    response = get_api(method, path, params, header, hostname, neutron_port)
    if response.status == 200:
        ports = json.loads(response.read())
        return ports
    if response.status == 400:
        error = 'Time out'
        return redirect(url_for('login', error=error))

# get lish network in your openstack 

def get_network(token, hostname, neutron_port):
    method = 'GET'
    params = ''
    path = '/v2.0/networks'
    header = {'Content-Type': 'application/json', 'X-Auth-Token': token}
    response = get_api(method, path, params, header, hostname, neutron_port)
    if response.status == 200:
        ports = json.loads(response.read())
        return ports
    if response.status == 400:
        error = 'Time out'
        return redirect(url_for('login', error=error))


if __name__ == '__main__':
    pass
