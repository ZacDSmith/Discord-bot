COMMANDS ARE NOT CASE SENSITIVE

event.py

    This creates the database (user_id, wallet, bank) if there isnt one and gives a first time chatter 100 currency

commands.py

    !bal returns wallet, bank, and networth
    !deposit {amount:int} allows you to deposit currency into bank from wallet
    !withdraw {amount:int} allows you to withdraw currency from bank to wallet
    !earn lets you earn money from a randint (1, 5)
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