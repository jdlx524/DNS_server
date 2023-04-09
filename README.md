# DNS_server
## Files
- dnsManager.py contains the class which wraps needed functions. 
- dns.py contains main function that sets socket connection. 
## Function
Run the command to start the socket connection:
```bash
sudo python3 dns.py
```
Then we can use another terminal to use the port given in dns.py to do DNS Lookup:
```bash
dig [url] @127.0.0.1
```
## Something remains to be improve
- While True consumes too much CPU. Maybe sleep time can be added to each loop.
- Parameters like:
```python3
QR = AA = '1'
TC = RD = RA = '0'
Z = '000'
RCODE = '0000'
```
They can also make difference. I think set default value can only be used in basic DNS_server.
