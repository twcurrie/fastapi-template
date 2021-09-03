## Migrations

### Alembic
Alembic provides for the creation, management, and invocation of change management scripts for a relational database, using SQLAlchemy as the underlying engine.  Migration scripts are listed within the `versions` directory in this directory, ordered sequentially by date of creation. 

### Current state
To identify the current revision on the database, you can execute the following command:
```bash
APP_DATABASE_URI=<endpoint> alembic current
```

### Performing schema migrations
To execute all the defined migrations on the database, you can execute the following command:
```bash
APP_DATABASE_URI=<endpoint> alembic upgrade head 
```
This will review the current state of the database migrations through a metadata table and execute all the known revision scripts after the current `revision id`.  The `revision id` is managed by alembic and stored in a metadata table on the database.

To execute the migrations on the database up to specific revision, you can execute the following command:
```bash
APP_DATABASE_URI=<endpoint> alembic upgrade <revision-id>
```

To execute the migrations on the database down to specific revision, you can execute the following command:
```bash
APP_DATABASE_URI=<endpoint> alembic downgrade <revision-id>
```
This command will rollback all migrations from the current `revision id` to the identified revision.


To execute the migrations on the database down to the seed schema, you can execute the following command:
```bash
APP_DATABASE_URI=<endpoint> alembic downgrade base 
```
This command will rollback all migrations. 


### Adding schema migrations
To add a new migration, execute the following command: 
```bash
alembic revision -m "<a short, but illucidating description>"
```
This will create a new revision script within the `versions` directory using the `script.py.mako` template file.  Update the `upgrade` and `downgrade` functions to perform the necessary steps for the migration using the [alembic](https://alembic.sqlalchemy.org/en/latest/api/operations.html#built-in-operation-objects) operations.


### Data migrations
Alembic is focused on schema migrations, but can support data migrations as well.  Data migrations can also be accomplished with alembic, but they generally need to leverage either the SQLAlchemy library with defined ORM models or execute bare SQL in order to modify the data in the table.