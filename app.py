from flask import Flask,session,render_template,url_for,redirect,request
from flask.ext.bootstrap import Bootstrap
import httplib,json

from common import get_api
from keystone_api import (get_token,get_endpoint,get_tenant_id,get_tenant_list)
from nova_api import (get_server_list,get_compute_list,get_compute_statistics,check_nova_service)

from neutron_api import (check_neutron_service,get_ports,get_network)
from datetime import datetime

## config email
mail_server = 'smtp.gmail.com'
mail_server_port = 587

#your mail
sender = ''
password_sender = ''
received = ''

#default Variable
username = None
password = None
tenant_name = 'admin'
SECRET_KEY = 'Welcome123'
hostname =None
error = None

#config port
keystone_port = 35357
nova_port = 8774
neutron_port = 9696


#config neutron
network_public_name='EXT1'
network_public_id=''
ip_used = 0
#config
app = Flask(__name__)
Bootstrap(app)
app.config.from_object(__name__)

@app.route("/login",methods=['GET','POST'])
def login():
    global username
    global password
    global hostname
    global error
    error = request.args.get('error')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hostname = request.form['hostname']
        token = get_token(tenant_name,username,password,hostname,keystone_port)
        session['logged_in'] = True
        session['token'] = token
        return redirect(url_for("index"))
    return render_template("login.html",error = error)

@app.route("/logout")
def logout():
    session.pop("logged_in",None)
    return redirect(url_for("login"))
@app.route("/reports",methods = ['GET','POST'])
def reports():
    token = session.get('token')
    alert =None
    if request.method =='POST':
        received = request.form['email']
        id_tenant_admin = get_tenant_id(token,hostname,keystone_port,'admin')
        compute_list = get_compute_statistics(id_tenant_admin,token,hostname,nova_port)

        cpu_used = compute_list['hypervisor_statistics']['vcpus_used']
        cpu_total = compute_list['hypervisor_statistics']['vcpus']
        ram_used = compute_list['hypervisor_statistics']['memory_mb_used']
        ram_total = compute_list['hypervisor_statistics']['memory_mb']
        hdd_free = compute_list['hypervisor_statistics']['free_disk_gb']
        hdd_total = compute_list['hypervisor_statistics']['local_gb']
        now = str(datetime.now())
        
        body = """
        Report at %s       
        CPU cores used: %d cores
        CPU cores Total: %d cores
        RAM Free: %d MB
        RAM Used: %d MB
        RAM Total: %d MB
        Disk Used: %d GB
        Disk Free: %d GB
        Disk Total: %d GB
        """ %(now,cpu_used,cpu_total,ram_total-ram_used,ram_used,ram_total,hdd_total - hdd_free ,hdd_free,hdd_total)
        if send_mail(mail_server,mail_server_port,sender,password_sender,received,body):
            alert = 'Sent mail successful'

    return render_template("reports.html",alert = alert)

@app.route("/services")
def services():
    token = session.get('token')
    id_tenant_admin = get_tenant_id(token,hostname,keystone_port,'admin')
    nova_service = check_nova_service(token = token,tenant_id =id_tenant_admin,username=username,password=password,hostname=hostname,keystone_port=keystone_port)
    neutron_agents = check_neutron_service(token= token,tenant_id = id_tenant_admin,username=username,password=password,hostname=hostname,keystone_port=keystone_port)
    return render_template("services.html",nova_service = nova_service,neutron_agents = neutron_agents)
@app.route("/ip")
def show_ip():
    token= session.get('token')

@app.route("/",methods=['GET','POST'])
def index():
    
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    token = session.get('token')
    if token != None:
        id_tenant_admin = get_tenant_id(token,hostname,keystone_port,'admin')
        compute_list = []
        list_node =get_compute_list(id_tenant_admin,token,hostname,nova_port)       
        for i in range(len(list_node['hypervisors'])):
            info = get_compute_list(id_tenant_admin,token,hostname,nova_port,str(list_node['hypervisors'][i]['id']))
            compute_list.append(info)
        ports  = get_ports(token,hostname,neutron_port)
        networks_list=get_network(token,hostname,neutron_port)
        
        for net in range(len(networks_list['networks'])):
            if networks_list['networks'][net]['name'] == network_public_name:
                global network_public_id
                network_public_id = networks_list['networks'][net]['id']
                global ip_used
                ip_used =0
                for ip in range(len(ports['ports'])):

                    if ports['ports'][ip]['network_id'] == network_public_id:
                        ip_used = ip_used+1                        
        return render_template("index.html",compute_list = compute_list,ip_used=ip_used)
    else:
        error = 'Time Out'
        return redirect(url_for('login', error = error))
    return render_template('index.html')
if __name__== '__main__':
    app.run(debug=True)
