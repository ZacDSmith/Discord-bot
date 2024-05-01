COMMANDS ARE NOT CASE SENSITIVE

Make sure to set up a .env file with the Token(Discord) and api key(Chatgpt). Check example.env for setup

Docs:

    https://discordpy.readthedocs.io/en/stable/
    https://docs.python.org/3/library/sqlite3.html
    https://pytube.io/en/latest/index.html
    https://platform.openai.com/docs/overview
    

event.py

    This creates the database with tables 
        main(user_id, wallet, bank), 
        items(name, price, description, id{primarykey}), 
        inv(user_id, item, id{primarykey}, count)
    When a user types in chat for the first time, they are rewarded 100 coins and a spot in the database.

commands.py

    !bal returns wallet, bank, and networth
    !deposit {amount:int} allows you to deposit currency into bank from wallet
    !withdraw {amount:int} allows you to withdraw currency from bank to wallet
    !mine lets you mine currency from a randint (1, 999)
    !gamble {amount:int} allows you to gamble currency above 10
    !slots {amount:int} lets you gamble currency in the form of a slot machine
  
shop.py

    !additem {item:str, price:int, description:str} allows you to add an item to the DB (ADMIN ONLY)
    !removeitem {item:str} allows you to remove an item from the DB (ADMIN ONLY)
    !shop displays items in the DB with name, price, description
    !buy {item:str} allows you to buy an item from the shop
    !sell {item:str} allows you to sell an item for currency
    !inv lets you check your inv for items you've purchased

chatbot.py

    !chat {prompt:str} response to a prompt entered by the user.

imageai.py

    !image {prompt:str} generates a image using prompt entered by the user.
