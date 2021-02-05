# Voronoi-Diagrams
Voronoi diagrams Fortune's Algorithm

```
git clone https://github.com/EderVs/Voronoi-Diagrams.git
```

In a new virtual environment install dependencies
```
pip install -r requirements.txt
```

Set `SECRET_KEY` env var
```
export SECRET_KEY="secret_key"
```

Install `voronoi-diagrams` package.
```
pip install -e .
```

Run web server
```
python vd_server/manage.py runserver
```
And the server will be running in the port 8000
