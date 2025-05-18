# Zscaler ZPA Connectors Zabbix Monitoring
Zabbix Zscaler ZPA Monitoring


## Requirements

- Python3 installed
- Python package `zscaler-sdk-python` installed
```
pip install zscaler-sdk-python
```

- Copy the Python script to Zabbix Server or Zabbix Proxy to the folder

```
cp zabbix_zscaler_connectors.py /usr/lib/zabbix/externalscripts
chmod +x /usr/lib/zabbix/externalscripts/zabbix_zscaler_connectors.py
```

## CLI Test

For testing purposes, you can execute

```
./zabbix_zscaler_connectors.py -cuid <CUSTOMER_ID> -clid '<CLIENT_ID_API>' -ckey '<CLIENT_SECRET_API>' -a get-connectors
```

*If works fine, you will see a JSON array with ZPA Connectors info. If you need to set the name of the ZScaler tenant (for identify customer), you can add `--client-name <CUSTOMER_NAME>`. A new field in JSON will appear with the name given.*

After that you can try to save the file to disk. Default folder is `/tmp`

```
./zabbix_zscaler_connectors.py -cuid <CUSTOMER_ID> -clid '<CLIENT_ID_API>' -ckey '<CLIENT_SECRET_API>' -a get-connectors --save-disk --folder .
```

If works fine, you will see a new file in the folder called connectors_<CUSTOMER_ID>.json. After that, you can ask for 1 ZPA Connector with

```
./zabbix_zscaler_connectors.py -cuid <CUSTOMER_ID> -clid '<CLIENT_ID_API>' -ckey '<CLIENT_SECRET_API>' -a get-connector -cid <CONNECTOR_ID> --folder <FOLDER>
```

If works fine, you will see a JSON output on console.

