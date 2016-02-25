# appfigure-slack
The parser for AppFigure RSS feed which posts the latest reviews into the Slack. 

# Configuration

1. Copy config.py.default as config.py
2. Set `webhoookUrl` as Webhook for your channel in Slack (in Songtive we have a separate channel for each app)
3. Set `rssUrl` for RSS from AppFigure "Reviews" section.
4. Create a new /etc/crontab record like that one:
```
0 10 * * * root cd /srv/reviews-agregator && python sender.py
```
   Restart `cron`, e.g. `service cron restart`

# FAQ

Q: Got error: `ImportError: No module named dateutil.parser` 

A: Install `python-dateutil`:
```
sudo apt-get install python-pip
sudo pip install python-dateutil pytz
```

# License

MIT

