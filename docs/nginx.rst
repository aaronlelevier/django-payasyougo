Nginx
=====

.. code-block::

    # make unix websocket executable
    chomod 0666 mysite.sock

    # test `conf` files
    nginx -t

    # START
    sudo /etc/init.d/nginx start
    sudo /etc/init.d/nginx restart
    sudo /etc/init.d/nginx stop



sudo /etc/init.d/nginx restart



MISC
----

.. code-block::

    # remove default
    rm /etc/init/sites-enabled/default

    # add mysite.conf to sites enabled
    ln -s /opt/django/mysite.conf /etc/nginx/sites-enabled/mysite.conf

    # collectstatic
    python /opt/django/mysite/manage.py collectstatic


nginx + uwsgi proxy test
------------------------

.. code-block::

    # port 9000 is forwarding to port 80

    http://uwsgi-docs.readthedocs.org/en/latest/tutorials/Django_and_nginx.html#nginx-and-uwsgi-and-test-py

    upstream django {
        server my.i.p.addr:9000 fail_timeout=0; 
    }
    server {
        listen 80;
        server_name example.com;

        location / {
            # uWSGI config
            uwsgi_pass mysite; # name of the `upstream` server
            include /opt/django/uwsgi_params; # the uwsgi_params file you installed
        }
    }

    # reload nginx and run w/ uwsgi
    sudo /etc/init.d/nginx restart
    uwsgi --socket :9000 --wsgi-file test.py


SSL
---

.. code-block::

    https://www.digitalocean.com/community/tutorials/how-to-create-an-ssl-certificate-on-nginx-for-ubuntu-14-04

    # cert location
    /etc/nginx/ssl/

    # key
    openssl genrsa -out /etc/nginx/ssl/mysite.com.key 2048

    # csr
    openssl req -new -sha256 -key /etc/nginx/ssl/mysite.com.key -out /etc/nginx/ssl/mysite.com.csr














