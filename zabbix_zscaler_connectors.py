#!/usr/bin/python3
#######################################################################################
# @author: Guille Rodriguez https://github.com/guillerg86
# @version: 2025-05-13 (YYYY-MM-DD)
# @python-version: 3.x
#
# This script allows for controlled retrieval of ZScaler ZPA Connectors information
#
#######################################################################################

import argparse
import json
from zscaler.oneapi_client import LegacyZPAClientHelper

def configure_parser():
    parser = argparse.ArgumentParser(prog="Zscaler Connectors API Monitoring")
    parser.add_argument("-cuid","--customer-id",type=int,required=True,help="Customer ID of the tenant")
    parser.add_argument("-clid","--client-id",required=True)
    parser.add_argument("-ckey","--client-secret",required=True)
    parser.add_argument("--cloud",choices=["PRODUCTION"],default="PRODUCTION",required=False)
    parser.add_argument("-a","--action",choices=["get-connectors","get-connector"],required=True)
    parser.add_argument("-f","--folder",default="/tmp",required=False)
    parser.add_argument("--save-disk",action="store_true")
    parser.add_argument("-cn","--client-name",required=False)
    parser.add_argument("-cid","--connector-id",required=False,help="Mandatory if action is 'get-connector'")
    parser.add_argument("--debug",action="store_true")
    return parser.parse_args()

def get_zpa_connection(client_id,client_secret,customer_id,cloud):
    return LegacyZPAClientHelper(client_id=client_id,
                            client_secret=client_secret,
                            customer_id=customer_id, 
                            cloud=cloud) 

def get_zpa_connectors(zpa_api):
    return zpa_api.connectors.list_connectors()[0]

if __name__ == "__main__":
    args = configure_parser()
    if args.debug:
        print(f"\tCustomerID: {args.customer_id}")
        print(f"\tClientId: {args.client_id}")
        print(f"\tClientSecret: {args.client_secret}")
        print(f"")

    if args.action == "get-connectors":
        zpa_api = get_zpa_connection(args.client_id,args.client_secret,args.customer_id,args.cloud)
        # Responde con un objeto tipo AppConnector, asi que sacamos el dict interno
        connectors = [vars(c) for c in get_zpa_connectors(zpa_api)]
        if args.client_name and len(args.client_name.strip()):
            for c in connectors:
                c['client_name'] = args.client_name
        if args.save_disk:
            with open(f"{args.folder}/connectors-{args.customer_id}.json", 'w') as fp:
                json.dump(connectors, fp, indent=2)
        else:
            print(json.dumps(connectors,indent=2))
    if args.action == "get-connector":
        if args.connector_id is None:
            print("Missing parameter --connector-id")
            exit(1)
        with open(f"{args.folder}/connectors-{args.customer_id}.json", 'r') as fp:
            connectors = json.load(fp)
        for connector in connectors:
            if connector.get('id') == args.connector_id:
                print(json.dumps(connector,indent=2))
                exit(0)
        print(f"Connector with id {args.connector_id} not found in file connectors-{args.customer_id}.json")

