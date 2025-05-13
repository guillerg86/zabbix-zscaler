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
    #parser.add_argument("-f","--folder",default="/tmp",required=False)
    #parser.add_argument("-cn","--client-name",required=False)
    #parser.add_argument("-cid","--connector-id",required=False,help="Mandatory if action is 'get-connector'")
    parser.add_argument("--debug",action="store_true")
    return parser.parse_args()

if __name__ == "__main__":
    args = configure_parser()
    if args.debug:
        print(f"\tCustomerID: {args.customer_id}")
        print(f"\tClientId: {args.client_id}")
        print(f"\tClientSecret: {args.client_secret}")
        print(f"")

    if args.action == "get-connectors":
        client = LegacyZPAClientHelper(client_id=args.client_id,
                                    client_secret=args.client_secret,
                                    customer_id=args.customer_id, 
                                    cloud="PRODUCTION") 
        # Responde con un objeto tipo AppConnector, asi que sacamos el dict interno
        connectors = [vars(c) for c in client.connectors.list_connectors()[0]]
        print(json.dumps(connectors,indent=2))
    ## TO-DO: Pendiente de poner que si va a disco duro, este consulte uno de los nodos en concreto.
    #if args.action == "get-connector":
    #    if args.connector_id is None:
    #        print("Missing parameter --connector-id")
    #        exit(1)

