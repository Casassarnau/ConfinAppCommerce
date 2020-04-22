<br>
<p align="center">
  <img alt="ConfinApp" src="https://github.com/Casassarnau/confinappComerce/blob/master/hackovid/static/favicon.png" width="200"/>
</p>
<br>

# Català

📝 App dissenyada per promocionar el comerç de proximitat - [Video demo](https://www.youtube.com/watch?v=9T0vEAJG4lQ&feature=youtu.be)

## Característiques

- Registre a partir d'un email ✉️
- Formulari per botiguers per registrar la seva botiga 📝
- Cerca de botigues per proximitat i ocupació	:mag:
- Control automatic dels estats de les compres 🔄
- Botiguers validen compres amb un QR 📱
- Emmagatzematge de les compres per poder fer una possible oferta cada 5 compres :purse:

## Configuració

Necessita: Python 3.X, virtualenv

- `git clone https://github.com/Casassarnau/confinappComerce.git`
- `virtualenv env --python=python3`
- `source ./env/bin/activate`
- `pip install -r requirements.txt`
- `python manage.py migrate`
- `python manage.py createsuperuser` (crea admin per administrar l'aplicació)

## Variables requerides de l'entorn (enviroment)

- **REGISTRATION_TOKEN**: Token que dona accès al comprador per poder-se registrar a la app

## Servidor

### Entorn local

- Configuració (vist previament)
- Configuració de les variables requerides de l'entorn (vist previament)
- `python manage.py runserver`
- Entra al teu navegador web, relaxa't i gaudeix!

### Rols d'usuari

- **is_client**: Usuari normal, pot fer compres i anar a comprar per acceptar-les
- **is_shopAdmin**: Deixa a l'usuari registrar una botiga i donar permisos als seus treballadors
- **is_admin**: Deixa entrar a la interficie d'Admin de Django

### Estil

- Colors i presentació: [static/style.css](static/style.css)
- Plantilla base i NavBar: [hackovid/templates/base.html](hackovid/templates/base.html)

### Contingut

#### Canvia la configuració dels formularis
Pots canviar el formulari: textos i camps a (app)/forms.py. Per exemple (shop): [shop/forms.py](shop/forms.py)

#### Canvia el teu model
Si necesites nous camps per els teus models

   - Actualitza els camps: app/models.py. Per example (shop): [shop/models.py](shop/models.py)
   - `python manage.py makemigrations`
   - Fes test i modifica les migracions per aixì no borrar la base de dades
   - `python manage.py migrate`
   
## UML
<br>
<p align="center">
  <img alt="ConfinApp" src="https://github.com/Casassarnau/confinappComerce/blob/master/UML-ca.png" width="100%"/>
</p>
<br>

## Llicència

MIT © Rita Geleta, Albeto López Sánchez, Arnau Cinca Roca i Arnau Casas Saez

- <a href="https://github.com/margaritageleta">@margaritageleta</a>
- <a href="https://github.com/catunlock">@catunlock</a>
- <a href="https://github.com/ArnauCinca">@ArnauCinca</a>
- <a href="https://github.com/Casassarnau">@Casassarnau</a>

# English

📝 App designed to promote local commerce - [Video demo](https://www.youtube.com/watch?v=9T0vEAJG4lQ&feature=youtu.be)

## Features

- Email sign up ✉️
- Shop Registration form for owners 📝
- Search less ocupied local shops nearby 	:mag:
- Automatic control of purchase expired, pending or accepted 🔄
- Personal shopper validates purchase with QR 📱
- Saves purchases in order to make a possible offer to the client :purse:

## Setup

Needs: Python 3.X, virtualenv

- `git clone https://github.com/Casassarnau/confinappComerce.git`
- `virtualenv env --python=python3`
- `source ./env/bin/activate`
- `pip install -r requirements.txt`
- `python manage.py migrate`
- `python manage.py createsuperuser` (creates super user to manage all the app)

## Available enviroment variables

- **REGISTRATION_TOKEN**: Token that gives acces to shop owners or workers to register in the app


## Server

### Local environment

- Set up (see above)
- Set Available enviroment variables (see above)
- `python manage.py runserver`
- Enter in your browser and enjoy!

### User roles

- **is_client**: Regular user. Can make a purchase and then go shop to accept it.
- **is_shopAdmin**: Allows user to register shop and give it acces to other shopAdmins
- **is_admin**: Allows user to enter Django Admin interface

### Style

- Colors and presentation: [static/style.css](static/style.css)
- Base template & Navbar: [hackovid/templates/base.html](hackovid/templates/base.html)

### Content

#### Update registration form
You can change the form, titles, texts in app/forms.py. For example (shop): [shop/forms.py](shop/forms.py)

#### Update your models
If you need extra labels for the app, you can change it and add your own fields.

   - Update model with specific fields: app/models.py. For example (shop): [shop/models.py](shop/models.py)
   - `python manage.py makemigrations`
   - Test & modify the migrations in order to don't delete any existent field from the data base.
   - `python manage.py migrate`
   
## UML
<br>
<p align="center">
  <img alt="ConfinApp" src="https://github.com/Casassarnau/confinappComerce/blob/master/UML-en.png" width="100%"/>
</p>
<br>

## License

MIT © Rita Geleta, Albeto López Sánchez, Arnau Cinca Roca i Arnau Casas Saez

- <a href="https://github.com/margaritageleta">@margaritageleta</a>
- <a href="https://github.com/catunlock">@catunlock</a>
- <a href="https://github.com/ArnauCinca">@ArnauCinca</a>
- <a href="https://github.com/Casassarnau">@Casassarnau</a>
