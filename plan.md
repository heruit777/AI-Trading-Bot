### AI Trading bot is self deployable because you need multi client api to execute orders of multiple users and you cannot test it out (as you don't access to another account), But I need to support multiple brokers like Dhan, Zerodha etc.

# Frontend
All the pages that you have built in the SEM 5 journal
1. Landing Page
2. Login Page
3. Dashboad Page
4. Trade History Page
5. Strategy Page
6. Reports Page
7. News Page
8. Broker Page (User guide on how to connect the a specific broker)

# Backend
1. web server (to handle the routes)
    - Following are the routes needed
    1. login/sign up (for frontend)
    2. Some data might require websocket connection as they will get updated in real time like PnL
    3. historical trading data (weekly, monthly, daily)
    4. Financial News
2. Bot Module
    1. Signal Detection Module (continously look for trade signals)
    2. Risk Management Module (To check whether a trade is following all the rules of Risk Management)
    3. Execution Module (Place orders(both enter and exit) to the user's broker)
    4. Monitoring Module (monitor the running trades)
    5. Logging Module 

# Database
1. MongoDB
2. InfluxDB (Time series)

# Machine Learning Framework
1. Tensorflow