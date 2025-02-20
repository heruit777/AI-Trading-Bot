To build the broker object for the user, want details I need (types Upstox and dummy)
For dummy I don't need anything
1. user_id
2. broker_type (upstox, dummy) [smallcase only converting to uppercase in backend]
3. access_token
4. api_version
5. api_key
6. api_secret

# Test Users Credentials
1. user1@gmail.com 12345678
2. user2@gmail.com 12345678
3. user3@gmail.com 12345678
4. harshnivande749@gmail.com with Google

# Todo
1. Fix the websocket issue on the dashboard anb Balance disable when websocket is connected.
2. Sometimes more than 4 trades are executed
![alt text](image.png)
# Dashboard
1. The issue is if I keep on switching tabs of dashboard then the websocket connects and disconnects so make that it doesn't disconnect when switching

# History
1. Calender view like bingx [Ignored]
2. All trades table

# Settings
1. A loader is required and also polish all the frontend. (Checkout typography in shadcn and use consistent color schema)