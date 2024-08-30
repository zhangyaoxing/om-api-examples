# om-api-alerts
Use API to configure Ops Manager alerts.

## Usage
### Script Configuration
The configuration are in the `config.json`. For now, only `om_url` is needed:
- `om_url`: Ops Manager base URL.

Ops Manager API `public_key` and `private_key` can also be stored in `config.json`. But saving the plain text key is not recommended. Instead, export them as environment variables before executing the script. For example: 
```bash
export public_key="<public_key>"
export private_key='<private_key>'
./set_alerts.py
```
The API key needs to be a global API key, which you can configure in Admin->API Keys. The key should have **one** the following roles:
- Global Monitoring Admin
- Global Owner

### Alerts Configuration
In general, common alerts should be configured as global alerts. Alerts that needs to be customized based on requirements of each project, are configured as project level alerts.

When you run the script, if a configured alert
- doesn't exist, it will be created.
- already exists, it will be updated.

#### Global Alerts
The configuration for global alerts are placed in the `./alerts` folder. Each `json` under this folder is an alert. Find them in the Admin->Alerts->Global Alert Settings.

#### Project Alerts
The project level alerts are configured in subfolders of `./alerts`, named by the `projectID`. For example,
```
./alerts/664322a90d6f3a4fd9b3be1b/
```
Each `json` under this folder will be an alert for the project `664322a90d6f3a4fd9b3be1b`.

#### New Alerts
If you want to create new alerts which you don't know how the payload (The `.json` files in the `./alerts`) looks like, an easy way is:
1. Create the alert from the UI
1. Use the following command to get all alerts from API
   ```bash
   # Global alert
   curl --user "<public_key>:<private_key>" --digest \
    --header "Accept: application/json" \
    --include \
    --request GET "http://<om_url>/api/public/v1.0/globalAlertConfigs"

   # Project alert
   curl --user "<public_key>:<private_key>" --digest \
    --header "Accept: application/json" \
    --include \
    --request GET "http://<om_url>/api/public/v1.0/groups/<project_id>/alertConfigs"
   ```
1. Find the payload you want and save the it into a new `.json` file.

Note: when you create new alerts, the file name doesn't matter. But we recommend that you use the `eventTypeName` or the `metricName` as file name for easy recognition. 

### Example Alerts Configured
The scripts comes with some global alerts, which uses our recommended thresholds. You can customize them based on your needs. There's also a `projectID` folder, which is used as an example to show you how project level alerts can be configured.

The thresholds of each alert are listed below:
- Global
  - Tickets
    - TICKETS_AVAILABLE_READS < 100, lasts 1min
    - TICKETS_AVAILABLE_WRITES < 100, lasts 1min
  - Replication Lag
    - OPLOG_SLAVE_LAG_MASTER_TIME > 20s, lasts 3min
  - Replication Oplog Window
    - OPLOG_MASTER_TIME < 48h, lasts 30min
  - Replica set has no Primary
    - NO_PRIMARY
  - Host is Down
    - HOST_DOWN
  - Replica set elected a new Primary
    - PRIMARY_ELECTED
  - System CPU (user %)
    - NORMALIZED_SYSTEM_CPU_USER > 80%, lasts 5min
  - Disk space used (%)
    - DISK_PARTITION_SPACE_USED_DATA > 70%
    - DISK_PARTITION_SPACE_USED_INDEX > 70%
  - Disk latency
    - DISK_PARTITION_READ_LATENCY_DATA > 20ms, lasts 1min
    - DISK_PARTITION_READ_LATENCY_INDEX > 20ms, lasts 1min
    - DISK_PARTITION_WRITE_LATENCY_DATA > 20ms, lasts 1min
    - DISK_PARTITION_WRITE_LATENCY_INDEX > 20ms, lasts 1min
  - Queued Readers/Writers
    - GLOBAL_LOCK_CURRENT_QUEUE_READERS > 20, lasts 1min
    - GLOBAL_LOCK_CURRENT_QUEUE_WRITERS > 20, lasts 1min
- Project
  - Opcounters
    - OPCOUNTER_QUERY > 1000, lasts 1min
    - OPCOUNTER_INSERT > 1000, lasts 1min
    - OPCOUNTER_DELETE > 1000, lasts 1min
    - OPCOUNTER_UPDATE > 1000, lasts 1min
    - OPCOUNTER_CMD > 1000, lasts 1min
  - WiredTiger Cache
    - CACHE_DIRTY_BYTES > 1000MB
    - CACHE_USED_BYTES > 1000MB
  - Connections
    - CONNECTIONS > 150
  - Query Targeting
    - QUERY_TARGETING_SCANNED_OBJECTS_PER_RETURNED > 1000, lasts 1min
    - QUERY_TARGETING_SCANNED_PER_RETURNED > 1000, lasts 1min
  - Average Execution Time
    - AVG_READ_EXECUTION_TIME > 150ms, lasts 1min
    - AVG_WRITE_EXECUTION_TIME > 150ms, lasts 1min