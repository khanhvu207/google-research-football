# Google Research Football with Manchester City F.C.

![gif](https://github.com/khanhvu207/google-research-football/blob/random-forest-v1/demo.gif)

This is my team's approach for the [Google Football competition on Kaggle](https://www.kaggle.com/c/google-football/overview). Our strongest agent has a rating of 1120 on the leaderboard (top 15%) although we didn't put much time into the contest.

## Summary of our strategy

We initially believed that rule-based approaches would be the way-to-go in this contest since building RL agents is pretty difficult, but it isn't the case in the later phase of the competition (top 5 are RL-based agents). We spent most of our time building and tweaking the rule-based bots, which was a critical mistake in these kind of contests since the global strategies among other teams changed rapidly throughout the timeline. 

Our final version used a mix of behavioural cloning, which is a simple ML classifier that was trained on top teams replays, and hard-coded defending strategy.

## Behavioural Cloning

This part is heavily inspired from [this notebook](https://www.kaggle.com/mlconsult/1149-ish-bot-rl-approximation). In a nutshell, approximately 15GB of replays was aggregated from the leaderboard and compiled into tabular form (Pandas Dataframe). With each pair of adjacent columns is the relative polar distance from the ball to the player, and the final column is agent's action, we tried several classification methods like Random forest, Gradient Boosting and Neural Nets to mimic top teams's player movements. We chose to use Catboost in the end due to its consistency and stabalized performance. 

## Defending strategy

It is easy to notice that defending is the most difficult part in the competition, perhaps Google designed it on purpose. We had several rules for passing and sliding, this is indeed not very robust but it gave a little boost to the overall rating. 
