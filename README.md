# Asset-tools
Asset tools - these tools are designed to export Device and User asset data into a comma seperated file.  We encourage customer feedback and contributions to this repository.  In the future we will expand this repository as the product expands in capability.

# Dependencies
- You require your JWT from the Sevco UI profile be added as an environment variable.  The JWT expires every 24 hours and the envirnment variable will need to be updated once it expires.

    $ export JWT="paste JWT here"

- You will also require your organization ID be added as an environment variable.  You can get the OrgID leveraging two different methods:
1. _curl -H "Authorization: $JWT" https://dev.api.sevcolabs.com/v1/admin/org -H "X-Sevco-Target-Org:$ORG" | jq_
2. Through the Sevco Shell by running _orgs info <index>_ and coping the OrgID value.

    $ export ORG="paste OrgID here"

# Execution
Run the scripts with _python devices.py_ or _python users.py_ as appropriate.  The devices.py script creates a file called devices.csv and users.py creates a file called users.csv.
