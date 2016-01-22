from common import get_api
from keystone_api import (get_token,get_endpoint,get_tenant_id,get_tenant_list)
import json
def get_volumes_list(tenant_id, token, hostname, cinder_port):