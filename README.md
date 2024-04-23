Discord bot with basic economy.
event.py:
This creates the database (user_id, wallet, bank) if there isnt one and gives a first time chatter 100 currency

commands.py:
  !bal returns wallet, bank, and networth
  !deposit allows you to deposit currency into bank from wallet
  !withdraw allows you to withdraw currency from bank to wallet
  !earn lets you earn money from a randint (1, 5)
  !gamble allows you to gamble currency above 10
  !slots lets you gamble currency in the form of a slot machine
  
shop.py:
!additem allows you to add an item to the DB (ADMIN ONLY)
!removeitem allows you to remove an item from the DB (ADMIN ONLY)
!shop displays items in the DB with name, price, description
!buy allows you to buy an item from the shop
!sell allows you to sell an item for currency
!inv lets you check your inv for items you've purchased
