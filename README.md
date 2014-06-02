# VoteIt Server

This is a server component for a VoteIt API — part of a suite of tools for managing parliamentary (or other) vote results. 

## Installation 

Before installing, make sure you have the following dependencies available on your system:

* MongoDB, ideally greater than 2.7.
* Python 2.7 and [virtualenv](http://www.virtualenv.org/en/latest/)

When you set up  ``voteit-server``, first check out the application from GitHub,
create a virtual environment and install the Python dependencies:

    git clone https://github.com/pudo/voteit-server.git
    cd voteit-server
    virtualenv env
    source env/bin/activate
    pip install -r requirements.txt
    python setup.py develop

If you're unfamiliar with virtualenv, be aware that you will need to 
execute the ``source env/bin/activate`` command each time you're working with
the project.

Next, you'll need to configure ``voteit-server``. Create a copy of the file ``voteit/default_settings.py``, as ``settings.py`` in the repository base. Open the file and set up the various account configurations. A particularly important setting is ``MONGODB_URI``, as it defines the database connection.

Once the new configuration is set up, you need to set an environment variable to point ``voteit-server`` at the configuration file:

    export VOTEIT_SETTINGS=`pwd`/settings.py

Finally, you can run ``voteit-server``. 

    python voteit/manage.py runserver 

## Bulk loader format

VoteIt data, conforming to the relevant Popolo specfication, can be loaded in bulk from a single JSON file. The file is expected to contain a dictionary with the following keys:

* ``motions`` - the actual motions, vote event and votes data.
* ``people`` - PopIt person data for each person that has cast votes.
* ``parties`` - PopIt organization data for each person that has cast votes.

Both ``people`` and ``parties`` are given as a dictionary in themselves, with the ID of each entity as the key, and their full representation as a value. 

The ``motions`` data is expected to be a list of fully nested VoteIt motion data, with a list of ``vote_events``, and ``votes`` within those. Each ``vote`` is expected to contain a ``option``, ``party_id`` and ``voter_id``. The latter two must resolve against the ``people`` and ``parties`` dictionaries specified in the root of the dictionary. 

To import a bulk votes file, execute the following command from within the ``voteit-server`` virtualenv: 

    python voteit/manage.py loadfile <file.json>

## API Documentation
 
* /api/1/motions
* /api/1/motion/`<motion_id>`
* /api/1/vote_events
* /api/1/vote_events/`<vote_event_id>`
* /api/1/parties
* /api/1/parties/`<party_id>`
* /api/1/persons
* /api/1/persons/`<party_id>`

