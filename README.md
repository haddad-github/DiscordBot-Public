# DiscordBot-Public
## Has 23 scripts, most are functional, some are currently on hold for some updates

##### Scripts in alphabetical order, their description and the modules used

1. AoE.py: Posts the unique units of the chosen Age of Empire civilization [Web Scraping | Selenium] - command: !aoe [civ]

2. animeRating: Posts the anime's rating/episodes/link to watch in embeded format [Web Scraping | BeautifulSoup] - command: !anime [anime]

3. camelcamel.py: Posts the item's graph of all-time prices as a picture [Web Scraping | lxml] - command !camel [item name]

4. coin.py: Posts the crypto coin's price, daily change and icon in embeded format [API request & Web Scraping | LiveCoinWatch & BeautifulSoup] - command: !coin [coin]

5. covid.py: Posts the COVID stats (infections, hospitalizations, deaths) as per the Government's official website [Web Scraping | BeautifulSoup] - command: !covid

6. currencyConvert.py: Converts a value in one currency to its value in another currency based on LIVE exchange rate [Utility & API request | ExchangeRate] - command: !convert [value] [from currency] [to this currency]

7. ethymology.py: Posts the etymology of the word based on etymonline [Web Scraping | BeautifulSoup] - command: !et [word]

8. flip.py: Flips a coin (heads or tail) [Utility] - command: !flip

9. gas.py: Posts average gas prices (ordinary, intermediary and premium) in the given city [Web Scraping | BeautifulSoup] - command: !gas [region]

10. grandexchange.py: Posts the name, icon, current price, today's price change, 30day/90day/180day price change of an Oldschool Runescape item [API request & Web Scraping | OSRS Api & BeautifulSoup] - command: !ge [item name]

11. leaguesTable.py: Posts the football(soccer) 5 main leagues current table standings [Web Scraping | BeautifulSoup] - command: !table [country]

12. meteo.py: Posts current local 8-days forecast weather [API request | OpenWeatherMap API] - command: !weather

13. mp3.py: Posts the .mp3 file of the video you've requested [Utility | youtube-dl] - command: !mp3 link

14. music.py: Bot enters the channel and streams the music requested (be it a link or a simple search) [Utility | youtube-dl] - command: !play [requested video or search]

15. odds.py: Calculates the odd of a specific event having happened (contextually used for item drops or events in videogames) [Utility] - command: !odds [number of times you got the time] [number of attempts] [item drop rate]

16. parcFoot.py: Posts the weekly schedule of the local park, allowing us to know when it's free to go play football(soccer) [Web Scraping | Selenium] - command: !foot

17. percentage.py: Calculates the % gain or % decrease between two values [Utility] - command: !percentage [from value] [to value]

18. post.py: Bot downloads the requested video and posts it as a .mp4 directly to the channel (ALSO SUPPORTS TIME INTERVALS) [Utility | youtube-dl] - command: !post [video link, be it youtube, instagram, tiktok, vimeo, etc.] [timestamp start (default=None)] [timestamp stop (default=None)]

19. reminder.py: (Currently not completed) Reminds someone about something they wanted in a specific time they requested [Utility] - command: !remindme [value] [time unit] [message]

20. run.py: (Currently limited usage for safety) Runs a python code written within discord itself and posts the results [Utility] - command: !run [python code]

21. steam.py: Posts the requested game's current price on Steam and whether there's a discount on it or not [Web Scraping | lxml] - command !steam [game name]

22. stock.py: Posts the stock price, daily change, high of the day, open price, previous close price and volume, including its icon [API request | yfinance API] - command: !stock [NASDAQ ticker]

23. trans.py: Translates a message from one language (auto-detected) into the requested language [API request | GoogleTranslate API] - command: !translate [target language] [original text]
