## Deployment Method 


## Heroku

Heroku has hobby dev tier subscription which allows developer to host hobby project.

1. Using Heroku CLI to deploy project.
2. Got domain name from Google Domains
3. Used Cloudfare for sake of SSL/TLS certificate.
4. Added Heroku DNS to google domains CNAME
5. Used Cloudfare Nameservers instead of google domains
6. Enabled DSSEC from cloudfare and had to disable google domains nameserver.