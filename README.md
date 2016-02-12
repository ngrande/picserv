# picserv
Small python webserver - only supports GET requests so far

- One can use this script to host a simple HTML site

---

### usage example
_[python3] picserv.py ./webres 127.0.0.1 80 443_

this will start two webservers (with address 127.0.0.1), one for port 80 and one for port 443 and both use the ./webres as their root path (where they look for the requested resources)

---
