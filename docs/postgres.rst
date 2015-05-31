Postgres
========

Output / Upload Database
------------------------
.. _docs: http://www.postgresql.org/docs/9.1/static/backup-dump.html

.. code-block::

    # output
    pg_dump -U <username> <db_name> > outfile.sql

    # upload
    # [note: make sure to switch to authorized database user first.  i.e. ``su postgres``]
    psql dbname < infile

    # to activate `psql`
    sudo su postgres

    # enter postgres command line (CL)
    psql

    # exit postgres CL

    # exit "postgres" user, and change back to root user
    exit


Allow remote access
-------------------
All configurations needed to run DB on a different server from the appserver,
or media server, etc...

.. code-block::

    # 1
    # to be able to trust remote server, add this
    # file: /etc/postgresql/9.3/main/pg_hba.conf
    # TYPE  DATABASE        USER            ADDRESS                 METHOD
    host    all             all             <server_ip>/32         md5

    # 2
    # what IP address(es) to listen on;
    # file: /etc/postgresql/9.3/main/postgresql.conf
    listen_addresses = '*'

    # 3
    # restart server
    /etc/init.d/postgresql restart

.. code-block:: python

    # 4
    # ./mysite/mysite/settings/prod.py

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', 
            'NAME': os.environ['DB_NAME'],
            'USER': os.environ['DB_USER'],
            'PASSWORD': os.environ['DB_PASSWORD'], 
            'HOST': os.environ['Db_SERVER_IP'], # DB server IP.  [ was prior-> 'localhost', ]
            'PORT': os.environ['DB_PORT'], # default is: '5432',
            'OPTIONS': {
                'autocommit': True,
                },
        }
    }
