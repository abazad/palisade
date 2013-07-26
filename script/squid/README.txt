Squid Auth for Oracle: Installation
===================================

1. Copy script to /home/bova/squid/bin/squid_ora_auth.py

2. chmod a+x /home/bova/squid/bin/squid_ora_auth.py

3. Edit /etc/squid/squid.conf or /etc/squid3/squid.conf::

	auth_param basic program /usr/bin/python /home/bova/squid/bin/squid_ora_auth.py
	auth_param basic children 5
	auth_param basic realm My-Org Squid Proxy
	auth_param basic credentialsttl 2 minute

