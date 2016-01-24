import json

from flask import url_for, redirect
from novaclient.client import Client as nova_client

from common import get_api
from keystone_api import (get_endpoint)

# get all instance in your openstack using tenant admin 

def get_server_list(tenant_id, token, hostname, nova_port):
    header = {'Content-Type': 'application/json', 'X-Auth-Token': token}
    method = 'GET'
    params = ''
    path = '/v2/' + tenant_id + '/servers/detail?all_tenants=1'
    response = get_api(method, path, params, header, hostname, nova_port)
    if response.status == 200:
        servers_list = json.loads(response.read())
        return servers_list
    if response.status == 400:
        error = 'Time out'
        return redirect(url_for('login'))

# get list compute node or details one compute node depend on node_id

def get_compute_list(tenant_id, token, hostname, nova_port, node_id=None):
    header = {'Content-Type': 'application/json', 'X-Auth-Token': token}
    method = 'GET'
    params = ''
    if not node_id:
        path = '/v2/' + tenant_id + '/os-hypervisors'
    else:
        path = '/v2/' + tenant_id + '/os-hypervisors/' + node_id
    response = get_api(method, path, params, header, hostname, nova_port)
    compute_list = response.read()
    if response.status == 200:
        compute_list = json.loads(compute_list)
        return compute_list
    if response.status == 400:
        error = 'Time out'
        return redirect(url_for('login'))

# get statistics all compute 

def get_compute_statistics(tenant_id, token, hostname, nova_port):
    header = {'Content-Type': 'application/json', 'X-Auth-Token': token}
    method = 'GET'
    params = ''
    path = '/v2/' + tenant_id + '/os-hypervisors/statistics'
    response = get_api(method, path, params, header, hostname, nova_port)
    if response.status == 200:
        compute_statistics = json.loads(response.read())
        return compute_statistics
    if response.status == 400:
        error = 'Time out'
        return redirect(url_for('login', error=error))

# get usage of each tenant depend on tenant admin and tenant which want to show

def get_tenant_usage(tenant_admin_id, tenant_id, token, hostname, nova_port):
    header = {'Content-Type': 'application/json', 'X-Auth-Token': token}
    method = 'GET'
    params = ''
    path = '/v2/' + tenant_admin_id + '/os-simple-tenant-usage/' + tenant_id
    response = get_api(method, path, params, header, hostname, nova_port)
    if response.status == 200:
        tenant_usage = json.loads(response.read())
        return tenant_usage
    if response.status == 400:
        error = 'Time out'
        return redirect(url_for('login', error=error))


# check service nova

def check_nova_service(token, tenant_id, username, password, hostname, keystone_port):
    nova_service = []
    status = {}
    compute_endpoint = get_endpoint('admin', 'nova', username, password, hostname, keystone_port)
    try:
        nova = nova_client('2', auth_token=token, bypass_url=compute_endpoint)
        services = nova.services.list()
        for service in services:
            status['type-name'] = service.binary
            status['status'] = service.status
            status['hostname'] = service.host
            status['state'] = service.state
            status['updated_at'] = service.updated_at
            status['zone'] = service.zone
            nova_service.append(status)
            status = {}
        return nova_service
    except Exception as e:
        error = str(e)
    return nova_service


if __name__ == '__main__':
    pass
