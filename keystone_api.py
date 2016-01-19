from common import get_api
import json
from flask import Flask,session,render_template,url_for,redirect,request
tenant_name='admin'
def get_token(tenant_name,username,password,hostname,keystone_port):
    header = {'Content-Type':'application/json'}
    params = json.dumps({"auth": {"tenantName":tenant_name,"passwordCredentials": {"username": username,"password": password}}})
    method ='POST'
    path = '/v2.0/tokens'
    response = get_api(method,path,params,header,hostname,keystone_port)
    if response.status == 200:
        data = json.loads(response.read())
        token = data['access']['token']['id']
        return token
    if response.status == 400:
        session['error'] = 'Incorect username/password check again'
        return redirect(url_for('login',error =error))
def get_endpoint(service,username,password,hostname,keystone_port):
    header = {'Content-Type':'application/json'}
    params = json.dumps({"auth": {"tenantName":tenant_name,"passwordCredentials": {"username": username,"password": password}}})
    method ='POST'
    path = '/v2.0/tokens'
    response = get_api(method,path,params,header,hostname,keystone_port)
    if response.status == 200:
        data = json.loads(response.read())
        for i in range(len(data['access']['serviceCatalog'])):
            if data['access']['serviceCatalog'][i]['name'] == service:
                endpoint = data['access']['serviceCatalog'][i]['endpoints'][0]['adminURL']
                return endpoint
    if response.status == 400:
        session['error'] = 'Incorect username/password check again'
        return redirect(url_for('login',error =error))
#def get_hostname_port(AUTH_URL):
def get_tenant_id(token,hostname,keystone_port,tenant_name):
    tenants_list = get_tenant_list(token,hostname,keystone_port)
    for i in range(len(tenants_list['tenants'])):
        if tenants_list['tenants'][i]['name'] == tenant_name:
            return tenants_list['tenants'][i]['id']
def get_tenant_list(token,hostname,keystone_port):
    header= {'Content-Type':'application/json','X-Auth-Token': token}
    method = 'GET'
    params = ''
    path = '/v2.0/tenants'
    response = get_api(method,path,params,header,hostname,keystone_port)
    if response.status == 200:
        tenants_list = json.loads(response.read())
        return  tenants_list
    if response.status == 400:
        error = 'Time out'
        return redirect(url_for('login'))              
if __name__ =='__main__':
    pass