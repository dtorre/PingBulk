# PingBulk

OVERVIEW

This is a very primative starting point for working with the PingOne Directory API, or "POD" for short. 

The POD API is an implementation of SCIM 1.1: System for Cross-domain Identity Management. 
However, at the time of this writing, POD does not have a "/bulk" endpoint as specified in the SCIM reference specification. 
Therefore, we have to step through create/update/delete operations one-by-one. These Python scripts help with that. 


AUTHENTICATION

You'll need to create a file that stores your API keys and secrets. The name of the file is "secrets.txt" and the format is:
ping.clientid={your_ping_client_id}
ping.apikey={your_ping_api_key}
