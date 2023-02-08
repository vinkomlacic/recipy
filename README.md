## Recipy - Recipe App (Django + Bootstrap)

Author: Vinko Mlačić

Recipy is an app that allows creating and publishing recipes. You can access
the live application at: 
[recipy.vinkomlacic.com](https://recipy.vinkomlacic.com). 

The app has set up authentication, so you will need an account. You can use the
demo account with the following credentials:
* username - _recipy_
* password - _recipy123_

The demo account has a limit on the amount of recipes that can be created and
its data is deleted on a daily basis.

### How to register an account
Registering an account is currently not supported. If you want to have one,
please get in touch with the developer at 
[vinkomlacic@outlook.com](mailto:vinkomlacic@outlook.com).

### Local development
For local development, you can use the SQLite database with the application.
This makes the setup very easy:
1. Clone this repository
2. Create a virtual environment
3. Install requirements: `pip install requirements/local.txt`
4. Copy `.envs/local_example.env` to `.envs/.env` and fill out the file
   according to the instructions
5. Run migrations: `python manage.py migrate`
6. Start the server: `python manage.py runserver`
