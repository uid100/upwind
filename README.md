## Upwind

```
5 meter long boats sailing upwind.

Boat A sailing 30 degrees 4.9 knots  =2.520 m/s

Boat B sailing 35 degrees 5.4 knots =2.778 m/s

Both boats sail to their respective lay lines A 30 degrees, B 35 degrees. They tack and sail to windward mark.

Which boat gets to the weather mark first and by how much?

.5 mile beat
.6 mile beat
.7 mile beat
.8 mile beat
.9 mile beat
```


my-flask-app/
│
├── app.py                # main Flask entry point
├── requirements.txt      # Python dependencies
├── runtime.txt           # optional, specify Python version
├── .deployment           # optional, custom startup command
└── .gitignore



az webapp config set \
    --resource-group myflask-rg \
    --name upwind \
    --startup-file "gunicorn --bind=0.0.0.0 --timeout 600 app:app"
