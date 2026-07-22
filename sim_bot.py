import os
import random
import statistics
from poker_dice import PokerDiceGame, _expert_best_keep_mc, _expert_best_category_v2, _remaining_categories, score_for_category

def sim_game():
    game = PokerDiceGame('test', 1, solo=True, difficulty=4)
    # play 13 turns
    for _ in range(13):
        p = game.players[2]
        remaining = _remaining_categories(p['scorecard'])
        dice = [random.randint(1, 6) for _ in range(5)]
        rolls = 2
        
        while rolls > 0:
            mask = game.get_keep_decision(dice, rolls)
            if mask == 31: # KEEP_ALL
                break
            # apply mask directly!
            dice = [dice[i] if (mask >> i) & 1 else random.randint(1, 6) for i in range(5)]
            rolls -= 1
            
        best_cat = _expert_best_category_v2(dice, remaining, p['scorecard'])
        p['scorecard'][best_cat] = score_for_category(dice, best_cat)
        
    return sum(v for v in game.players[2]['scorecard'].values() if v is not None)

scores = [sim_game() for _ in range(10)]
print("Avg:", statistics.mean(scores))
print("Min:", min(scores))
print("Max:", max(scores))
