Dogecoin Alexa Skill
====================
Such Echo, Much Alexa, Very Amazon, Wow

An Alexa Skill for Amazon Echo to fetch the current Dogecoin price.

Based on https://github.com/zpriddy/ZP_EchoNestPy


Running
-------

The DogeCoin skill is provided as a Docker container. To run it:

    docker run -d -p 8000:8000 --restart=always servercobra/dogecoin

For testing, you'll need to [create a self signed cert](https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/testing-an-alexa-skill#Configuring%20Your%20Web%20Service%20to%20Use%20a%20Self-Signed%20Certificate).

Save the key as `/etc/nginx/doge.key` and the certificate as `/etc/nginx/doge.crt`.

You'll need to set up an Nginx server in front of the Docker container. Edit 
`/etc/nginx/sites-enabled/dogecoin`:

    server {
            listen 443 ssl default_server;
            listen [::]:443 ssl default_server;
    
            server_name doge.nang.in;
            ssl_certificate     doge.crt;
            ssl_certificate_key doge.key;
            ssl_protocols       TLSv1 TLSv1.1 TLSv1.2;
            ssl_ciphers         HIGH:!aNULL:!MD5;
    
            location / {
                    include uwsgi_params;
                    uwsgi_pass 127.0.0.1:8000;
            }
    }

Then reload Nginx:

    /etc/init/nginx reload
    

Register
--------

You'll need to [register your skill with Amazon](https://developer.amazon.com/edw/home.html#/skills) 
to test and publish

When registering your skill, you can use the values from `intentSchema.json` and
`sampleUtterances.txt` when filling in 'Interaction Model'.


Building
--------

The app runs in a Docker container for simplicity. Make sure you have Docker
installed and up to date.

    docker build -t dogecoin .
