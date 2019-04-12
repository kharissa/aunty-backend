# Aunty Backend Template

## Download Repo
```
git clone git@github.com:kharissa/aunty-backend.git
```

## Create conda environment
```
conda create -n "aunty_backend"
```

## Install Dependencies

1. Delete `peewee-db-evolve==3.7.0` from `requirements.txt` during the first installation.

2. Run:
   ```
   pip install -r requirements.txt
   ```
3. Now add `peewee-db-evolve==3.7.0` back into `requirements.txt`
4. Run again:
   ```
   pip install -r requirements.txt
   ```
5. Restart your terminal as well and reactivate conda source

6. Create a `.env` file at directory root.

7. Enter the following in your terminal to generate a random secret key.

```
python -c 'import os; print(os.urandom(32))'
```

8. Add the following variables into your `.env` file.

```
FLASK_APP='start'
FLASK_ENV='development'
DATABASE_URL="postgres://localhost:5432/aunty_dev"
SECRET_KEY='YOUR_SECRET_KEY'
DB_TIMEOUT=300
DB_POOL=5
```

9. Create a PostgresQL Database**

```
createdb aunty_dev
```

10. Create a `.gitignore` file to ignore sensitive information being uploaded into GitHub.
```
.vscode
*.DS_Store
*__pycache__
*.env
```

11. Run a database migration
```
python migrate.py
```

## Start Working

1. Create a branch
```
git checkout -b <feature-name>
```
2. Start making changes
```
git add <changed_file_name>
git commit -m "Added <something> to <somewhere>"
```
3. Push changes to your branch
```
git push origin <feature-name>
```

## Starting Server

```
flask run
```

## Starting Shell

```
flask shell
```