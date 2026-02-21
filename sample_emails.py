past_emails = [
    {
        "query": "Hi team, file transfer to partner ABC failed with error code 550. Can you check?",
        "reply": "Hi, we checked the MFT logs and found that partner ABC's SFTP credentials expired. We have reset the password and coordinated with the partner. Please retry the transfer — it should work now."
    },
    {
        "query": "Partner XYZ is not receiving our outbound files since yesterday. Please investigate.",
        "reply": "Hi, we identified that the AS2 connection to partner XYZ had a certificate mismatch. We have renewed the certificate and tested the connection successfully. Files should now be delivered normally."
    },
    {
        "query": "Getting timeout error when sending files to Hartford. Error: Connection timed out after 30s.",
        "reply": "Hi, the timeout was caused by a firewall rule change on Hartford's end blocking our IP. We have raised the issue with their IT team and they have whitelisted our IP. Connection is now restored."
    },
    {
        "query": "EDI 850 purchase order file is failing validation. Can you check what's wrong?",
        "reply": "Hi, we checked the file and found that segment ISA16 had an incorrect delimiter character. We have corrected the BIC mapping and reprocessed the file successfully. Future files will be handled automatically."
    },
    {
        "query": "Partner DEF says they are receiving duplicate files. Please check our MFT configuration.",
        "reply": "Hi, we found that the retry mechanism was incorrectly configured with a 0-minute interval, causing duplicate sends. We have updated the retry interval to 30 minutes and removed the duplicate files from partner DEF's inbox."
    },
    {
        "query": "OFTP connection to European partner GHI is failing. Error: Authentication failed.",
        "reply": "Hi, the OFTP authentication failure was due to an expired OFTP certificate on our side. We have renewed the certificate and re-established the connection. Please confirm with partner GHI that they are now receiving files."
    },
    {
        "query": "File transfer is stuck in pending state for 2 hours. Partner JKL is waiting.",
        "reply": "Hi, we found that the MFT processing queue had a stuck thread. We restarted the relevant service and the pending transfers have been processed. Partner JKL's files have been delivered successfully."
    },
    {
        "query": "EDI 997 acknowledgement is not being received from partner MNO. Is there an issue?",
        "reply": "Hi, partner MNO updated their acknowledgement endpoint without notifying us. We have updated the endpoint in our Seeburger configuration and acknowledgements are now being received correctly."
    },
    {
        "query": "Getting error: File size exceeds maximum limit when sending to partner PQR.",
        "reply": "Hi, partner PQR has a 10MB file size limit on their SFTP server. The file being sent was 15MB. We have configured automatic file splitting in Seeburger BIS and the transfer has completed successfully."
    },
    {
        "query": "Partner STU is complaining that files are arriving 3-4 hours late. Can you investigate?",
        "reply": "Hi, we found that the scheduled job for partner STU was set to run every 4 hours instead of every 30 minutes. We have corrected the schedule and files are now being delivered on time."
    },
    {
        "query": "New trading partner VWX onboarding — they use AS2 protocol. What information do we need?",
        "reply": "Hi, for AS2 onboarding we need the following from partner VWX: AS2 ID, AS2 URL endpoint, their public certificate, MDN settings (sync or async), and preferred encryption algorithm. Please request these details and we will configure Seeburger accordingly."
    },
    {
        "query": "EDIFACT ORDERS message failing with error: Invalid UNB segment.",
        "reply": "Hi, the UNB segment error was caused by an incorrect interchange sender ID in the mapping. We have corrected the BIC mapping and reprocessed the file. The ORDERS message has been delivered to the partner successfully."
    },
    {
        "query": "Partner YZA switched to FTPS from FTP. Our transfers are now failing.",
        "reply": "Hi, we have updated partner YZA's connection profile in Seeburger BIS from FTP to FTPS and imported their server certificate. Test transfer was successful. All future transfers will use the secure FTPS connection."
    },
    {
        "query": "Getting 'unknown partner' error for incoming files from partner BCD.",
        "reply": "Hi, partner BCD recently changed their AS2 sender ID without prior notice. We have updated their partner profile in Seeburger to reflect the new ID. Incoming files from BCD are now being processed correctly."
    },
    {
        "query": "File transformation failing for X12 810 invoice. Mapping error in BIC.",
        "reply": "Hi, we found a null value handling issue in the BIC mapping for the N1 segment of the X12 810. We have updated the mapping to handle optional fields correctly and reprocessed the invoice successfully."
    },
    {
        "query": "MFT server is showing high CPU usage since morning. Performance is degraded.",
        "reply": "Hi, we identified a runaway process caused by a large batch of files queued simultaneously. We have cleared the backlog, optimized the batch size settings, and CPU usage is back to normal levels."
    },
    {
        "query": "Partner EFG needs test environment setup for UAT. Can we configure a test profile?",
        "reply": "Hi, we have created a separate test profile for partner EFG in our non-production Seeburger environment. Test AS2 endpoint and credentials have been shared with partner EFG. UAT can begin immediately."
    },
    {
        "query": "Receiving malformed XML files from partner HIJ. Transformation is failing.",
        "reply": "Hi, the XML files from partner HIJ have a missing namespace declaration which is causing the transformation failure. We have raised this with partner HIJ's technical team and they will fix the source files. As a workaround we have added namespace handling in our mapping."
    },
    {
        "query": "Need to add a new file type CSV to existing partner KLM profile. How long will it take?",
        "reply": "Hi, adding CSV file type support to partner KLM's profile requires a new BIC mapping and profile update in Seeburger. Estimated time is 2 business days. Please share the CSV file specification and we will begin configuration."
    },
    {
        "query": "Partner NOP reports that files received are corrupted. Zip file extraction fails.",
        "reply": "Hi, we found that the compression settings in Seeburger were using a zip format incompatible with partner NOP's extraction tool. We have changed the compression to standard zip and partner NOP has confirmed successful extraction."
    },
    {
        "query": "SLA breach alert — partner QRS has not received files for 6 hours.",
        "reply": "Hi, we identified that partner QRS's SFTP server had a disk full error preventing file delivery. We have notified their team who cleared disk space. All pending files have been delivered and SLA breach has been documented."
    },
    {
        "query": "What is the status of the monthly EDI reconciliation report for Hartford?",
        "reply": "Hi, the monthly EDI reconciliation report for Hartford is currently being generated. It will be available by end of business today. The report will cover all X12 transactions processed in the current month including 850, 855, and 810 messages."
    },
    {
        "query": "Partner TUV wants to change file delivery from pull to push model. Is this possible?",
        "reply": "Hi, yes we can switch partner TUV from pull to push model. We will need their SFTP server details, credentials, and target directory path. Once provided we can complete the configuration change within 1 business day."
    },
    {
        "query": "Getting SSL handshake failure when connecting to partner WXY's HTTPS endpoint.",
        "reply": "Hi, the SSL handshake failure was due to TLS version mismatch — partner WXY upgraded to TLS 1.3 while our connector was configured for TLS 1.2. We have updated the connector configuration and the HTTPS connection is now working."
    },
    {
        "query": "EDI 856 ASN file from partner ZAB is missing mandatory segments. How to handle?",
        "reply": "Hi, the missing mandatory segments in partner ZAB's 856 ASN indicate a mapping issue on their side. We have sent them the EDI specification highlighting the required segments. As a temporary measure we have added default values for missing segments in our inbound mapping."
    },
    {
        "query": "Need to set up PGP encryption for file transfers with partner CDE. What are the steps?",
        "reply": "Hi, for PGP encryption setup with partner CDE we need to exchange public keys. Please request partner CDE's PGP public key and share ours with them. Once keys are exchanged we will configure PGP encryption in Seeburger BIS within 1 business day."
    },
    {
        "query": "Partner FGH is sending files in wrong format. We are expecting EDIFACT but receiving flat file.",
        "reply": "Hi, we have contacted partner FGH and confirmed this is a configuration error on their end. They have corrected their system to send EDIFACT format. We have also added format validation in our inbound processing to catch such issues in future."
    },
    {
        "query": "MFT job for partner IJK failed with OutOfMemory error at 2 AM.",
        "reply": "Hi, the OutOfMemory error was caused by an unusually large file batch sent by partner IJK overnight. We have increased the JVM heap size for the MFT service and added file size alerting. The failed job has been rerun successfully."
    },
    {
        "query": "Partner LMN wants audit logs of all file transfers for last 30 days. How to get these?",
        "reply": "Hi, we have extracted the MFT audit logs for partner LMN covering the last 30 days from Seeburger BIS. The report includes file name, transfer timestamp, status, and byte count for all transfers. Report has been sent to your email."
    },
    {
        "query": "Urgent — production file transfer to Hartford completely stopped. No files processing.",
        "reply": "Hi, we identified a Seeburger BIS service outage caused by a database connection pool exhaustion. We have restarted the service, increased the connection pool size, and all queued files are now processing. Root cause analysis will be shared within 24 hours."
    },
]