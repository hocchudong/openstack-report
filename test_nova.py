from keystone_api import (get_token,get_endpoint,get_tenant_id,get_tenant_list)
username='admin'
password='Welcome123'
hostname='172.16.69.60'
keystone_port=35357
compute_endpoint_admin = get_endpoint('admin','nova',username,password,hostname,keystone_port)
compute_endpoint_demo = get_endpoint('demo','nova',username,password,hostname,keystone_port)

from novaclient.client import Client as nova_client

token =get_token('admin',username,password,hostname,keystone_port)
nova = nova_client('2',auth_token=token,bypass_url=compute_endpoint_admin)

print "instance in  tenant admin"
print nova.servers.list()

token = get_token('demo',username,password,hostname,keystone_port)
nova = nova_client('2',auth_token=token,bypass_url=compute_endpoint_demo)

print "instance in tenant demo"
print nova.servers.list()
for server in nova.servers.list():
	print nova.servers.ips(server)
