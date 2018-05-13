# story-emojis-telegram-bot
A telegram bot for you to play story emojis (just the same as story cubes but with emojis!)

## Deployment on [Heroku](https://www.heroku.com/home)

```
heroku login
heroku create --region us appname
heroku buildpacks:set heroku/python # set python buildpack
git push heroku master # deploy app to heroku
heroku config:set TELEGRAM_TOKEN=<YOUR-TOKEN> # set config vars, insert your own
```

To start the bot, run: `./start.sh`.
To stop the bot, run: `./stop.sh`.
