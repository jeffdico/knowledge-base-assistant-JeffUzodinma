# Knowledgebase app by Jeff Uzodinma

## Env settings

> *DYNACONF_DATABASE_URI*   _database connection strings_
 
> *DYNACONF_STATIC_FOLDER*      _defaults to frontend/app/dist/assets/_
 
> *DYNACONF_TEMPLATE_FOLDER*      _defaults to frontend/app/dist folder_

> *DYNACONF_TZ*    _Default timezone_

> *DYNACONF_DBLOGGER* _database error logname_        

> *DYNACONF_APPLOGGER*   _application error logname_

> *DYNACONF_AI_KEY*    _AI secret key_

> *DYNACONF_AI_MODEL*   _AI model name_

> *DYNACONF_AI_TEXT_EMBEDED*  _AI text_embeded model_

> *DYNACONF_ENV*  _env configuration_

## First time steps 

### `python3 -m venv venv` 

### `source venv/bin/activate` _(linux - ubuntu command)_ 
 
### `pip install -r requirements.txt`

###  `./start-server/sh`  _to start the flask application_

### `./apply_fixtures.sh`  _a bash shell executable script to initialize the folders and database data run on mac and linux only, otherwise run manually_



