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

## Template

### Items (1)
- Connectors raw data

### Items prototype (25)
- Connected since (last_broker_connect_time)
- Connector group id
- Connector group name
- Control broker name
- Control channel status
- Current version
- Current version (string)
- Enabled
- Expected version
- Fingerprint
- Last disconnection
- Last upgrade date (timestamp)
- Latitude
- Location
- Longitude
- Modified by user id
- Modified time
- Platform
- Platform details
- Previous version
- Private IP address
- Public IP address
- Raw data
- Upgrade attempts
- Upgrade status


### Triggers prototype (4)

|Trigger Level|Trigger Name|
|-|-|
|Warning|{#ZSCALER.CONNECTOR.NAME}: Disconnected|
|Warning|{#ZSCALER.CONNECTOR.NAME}: Enabled status changed to disabled|
|Information|{#ZSCALER.CONNECTOR.NAME}: Upgrade available|
|Information|{#ZSCALER.CONNECTOR.NAME}: Upgrade status|

### Macros (4)

- {$ZSCALER.ZPA.CUSTOMER_ID}
- {$ZSCALER.ZPA.CLIENT_ID}
- {$ZSCALER.ZPA.CLIENT_SECRET}
- {$ZSCALER.CONNECTOR.ZPA.MIN_VERSION} - Not used at this moment

## ZScaler Private Access Configuration

Access to your tenant **Administration > Private Access Tenant** to get your **Tenant ZPA ID** (there is a field with this name), you will use this as the value of *{$ZSCALER.ZPA.CUSTOMER_ID}* macro.

After that, go to **Administration > API Configuration > Legacy API > Private Access API** and create new API, grab the client ID and Client Secret, this will be used as the value of *{$ZSCALER.ZPA.CLIENT_ID}* and *{$ZSCALER.ZPA.CLIENT_SECRET}* macros. 

Now test with CLI and save it for later (you will need to configure zabbix-host)


## CLI Test

For testing purposes, you can execute

```
python3 -B zabbix_zscaler_connectors.py -cuid <TENANT_ZPA_ID> -clid '<CLIENT_ID_API>' -ckey '<CLIENT_SECRET_API>' -a get-connectors
```

If works fine, you will see a JSON array with ZPA Connectors info. *If you need to set the name of the ZScaler tenant (for identify customer), you can add `--client-name <CUSTOMER_NAME>`. A new field in JSON will appear with the name given.*

After that you can try to save the file to disk. Default folder is `/tmp`

```
python3 -B zabbix_zscaler_connectors.py -cuid <TENANT_ZPA_ID> -clid '<CLIENT_ID_API>' -ckey '<CLIENT_SECRET_API>' -a get-connectors --save-disk --folder .
```

If works fine, you will see a new file in the folder called connectors_<CUSTOMER_ID>.json. After that, you can ask for 1 ZPA Connector with

```
python3 -B zabbix_zscaler_connectors.py -cuid <TENANT_ZPA_ID> -clid '<CLIENT_ID_API>' -ckey '<CLIENT_SECRET_API>' -a get-connector -cid <CONNECTOR_ID> --folder <FOLDER>
```

If works fine, you will see a JSON output on console.

## Installing script on Zabbix Server or Proxy

Copy the script file to zabbix external scripts folder inside Zabbix Server or Zabbix Proxy 

```
mv zabbix_zscaler_connectors.py /usr/lib/zabbix/externalscripts/
```

Change permisions (add +x)

```
chmod +x /usr/lib/zabbix/externalscripts/zabbix_zscaler_connectors.py 
```

## Configuring Host on Zabbix

Create a new host.
 
<table>
<tr><th>Hostname</th><td>Set the hostname you want</td></tr>
<tr><th>Templates</th><td>Template Zscaler ZPA <- This template... </td></tr>
<tr><th>Interfaces</th><td>Add Agent interface -> Set IP 127.0.0.1</td></tr>
<tr><th>Monitored by</th><td>Server or Proxy (& select the proxy)</td></tr>
</table>

On Macros tab, set macro names and values

|Macro name|Macro value|Description|
|-|-|-|
|{$ZSCALER.ZPA.CUSTOMER_ID}|TENANT_ZPA_ID|***Administration > Private Access Tenant > Tenant ZPA ID***|
|{$ZSCALER.ZPA.CLIENT_ID}|CLIENT_ID_API|API credentials from ***Administration > API Configuration > Legacy API > Private Access API***|
|{$ZSCALER.ZPA.CLIENT_ID}|CLIENT_SECRET_API|API credentials from ***Administration > API Configuration > Legacy API > Private Access API***|

Save the new host, go to the **Host -> Discovery Rules** and execute **ZPA Connectors Discovery rule**. After few seconds all ZPA Connectors will appear inside host.

Remember, if you are setting monitoring by proxy, you need to wait more time (proxy sync...) or you can restart service on proxy to force a sync with server.


