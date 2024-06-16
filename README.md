# BotBattle Online Judge

Online judge code tester. Bot Battle is a platform where coders can build and battle their bots made for traditional games like Connect 4, Uno, among others.

## Upload for testing (Code files)

1. Receive challenge identifier, code file, language identifier.
2. Create docker image with specifications
3. Run container with cross application input/output
4. Repeat step 3 several times
5. Process results

# Heads-Up Poker

At the start of each game each player will receive:
`0 [User ID] [Big Blind] [Small Blind]`

At the start of each round, each player will receive:
`0 0 [Card 1 Number] [Card 1 Suit] [Card 2 Number] [Card 2 Suit] [Player With Seat Button] [Player 1's Money Pool] [Player 2's Money Pool]`
The initial bet will be discounted from each player's money pool at the start of each round.
`1 <= Card Number <= 13`, where 1 is A, 2-10 is the corresponding number card, 11 is Jack, 12 is Queen, 13 is King
`Card Suit \in {S, H, D, C}`, where S is spades, H is hearts, D is diamonds, C is clubs

During the round, a player may receive one of the three following inputs:
`0 1 [Table Card Number] [Table Card Suit]`

`0 2 [Current Bet]`
This is the only command that requires a response from the player
- If Response Bet >= Player's Money Pool, the player `All-In`s.
- Else If Response Bet < Current Bet, the player Folds
- Else If Response Bet = Current Bet, the player Checks
- Else If Response Bet > Current Bet, the player Raises

If at any time, the player return invalid input, the hand ends and the other player wins the round

The game end after one of the following conditions are meet
- A player is unable to pay their initial bet
- A 100 hands habe been delt

`0 3 [Winner Player ID]`


# Poker commands

At the start of each game, each player will receivce `` which indicate the initial money pool each player has, and the big and small blind bets.
```
0 [User ID] [Number of Players] [Big Blind] [Small Blind]
```

At the start of each round, each player will receive:  
```
0  [Card] [Card]
[Big Blind User ID] [Small Blind User ID]
For ID in [1..N] in order of betting:
[ID] [ID's Money Pool]
```

, which indicates the user's ID, the number of player in the table, and the money available to the player. Each player has an ID in the range `[1..N]`. In the first round, each player will have the same money pool and the amount will be updated correspondingly. For the big and small blind, both initial bets will be removed from their balance since the start of the round.

For the rest of the round, the player will receive some the following commands:
| Input Structure             | Expected Output Structure |
|-----------------------------|---------------------------|
|`0 0 [Card] [Card]`| `None`  |
|`[Own User ID] [Current Bet]`| `[User Bet >= User Bet]`  |

[User ID]