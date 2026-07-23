"""
Test poker_dice.py scoring and bot category/keep logic for the specific
dice sets described in the user's bug report.

Usage:
    python3 test_pd_scoring.py
"""

import sys
import os

# Ensure we can import from the project root
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from poker_dice import (
    score_for_category,
    _expert_best_category_v2,
    _bot_choose_category,
    _remaining_categories,
    CATEGORY_IDS,
    _expert_leaf_bonus,
    _expert_best_keep_mc,
    _keep_candidates,
)


def build_empty_scorecard():
    """Return a scorecard where every category is still available (None)."""
    return {c: None for c in CATEGORY_IDS}


# =========================================================================
# 1. Score table for [1, 1, 6, 4, 6]  (user's reported after-roll-3 dice)
# =========================================================================
DICE_A = [1, 1, 6, 4, 6]

# =========================================================================
# 2. Score table for [1, 1, 6, 6, 6]  (what the bot "recorded")
# =========================================================================
DICE_B = [1, 1, 6, 6, 6]

# =========================================================================
# 3. Roll-2 state for keep-candidate analysis
# =========================================================================
DICE_ROLL2 = [1, 2, 6, 4, 6]


def compute_scores(dice):
    """Compute score_for_category for every category."""
    return {cat: score_for_category(dice, cat) for cat in CATEGORY_IDS}


def print_table(scores_a, scores_b):
    """Print a formatted comparison table."""
    header = f"{'Category':<20} | {'Score [1,1,6,4,6]':<18} | {'Score [1,1,6,6,6]':<18}"
    sep = "-" * len(header)
    print(sep)
    print(header)
    print(sep)
    for cat in CATEGORY_IDS:
        sa = scores_a[cat]
        sb = scores_b[cat]
        print(f"{cat:<20} | {str(sa):<18} | {str(sb):<18}")
    print(sep)


def test_score_tables():
    """Test 1 & 3: verify score_for_category for both dice sets."""
    print("\n" + "=" * 70)
    print("TEST 1 & 3: score_for_category for both dice sets")
    print("=" * 70)

    scores_a = compute_scores(DICE_A)
    scores_b = compute_scores(DICE_B)
    print_table(scores_a, scores_b)

    # -- Dice A assertions --
    # full_house must be 0 because [1,1,6,4,6] is two pair, not full house
    assert scores_a['full_house'] == 0, (
        f"DICE_A full_house expected 0, got {scores_a['full_house']}"
    )
    print("\n[DICE_A] full_house = 0  .......... PASS")

    # -- Dice B assertions --
    # full_house must be 25 because [1,1,6,6,6] is trips + pair
    assert scores_b['full_house'] == 25, (
        f"DICE_B full_house expected 25, got {scores_b['full_house']}"
    )
    print("[DICE_B] full_house = 25 ......... PASS")

    return scores_a, scores_b


def test_bot_choose_category(scores_a, scores_b):
    """Test 2 & 4: verify _bot_choose_category picks for both dice sets."""
    print("\n" + "=" * 70)
    print("TEST 2 & 4: _bot_choose_category (all categories remaining)")
    print("=" * 70)

    scorecard = build_empty_scorecard()
    remaining = _remaining_categories(scorecard)

    cat_a = _bot_choose_category(DICE_A, remaining, scorecard)
    cat_b = _bot_choose_category(DICE_B, remaining, scorecard)
    print(f"[DICE_A] _bot_choose_category => {cat_a!r}")
    print(f"[DICE_B] _bot_choose_category => {cat_b!r}")

    # For DICE_A ([1,1,6,4,6]), the highest marginal-value category is expected
    # to be 'two_pairs' (score=18), 'chance' (score=18), or 'pair' (score=18)
    # since it's a two-pair hand. Let's check the actual scores:
    print(f"  scores_a['two_pairs']={scores_a['two_pairs']}, "
          f"scores_a['chance']={scores_a['chance']}, "
          f"scores_a['pair']={scores_a['pair']}, "
          f"scores_a['sixes']={scores_a['sixes']}")
    print(f"  scores_b['full_house']={scores_b['full_house']}, "
          f"scores_b['three_of_kind']={scores_b['three_of_kind']}, "
          f"scores_b['chance']={scores_b['chance']}, "
          f"scores_b['sixes']={scores_b['sixes']}")

    print("PASS (no crash, values printed)")


def test_expert_best_category_v2(scores_a, scores_b):
    """Test 2 & 4: verify _expert_best_category_v2 for both dice sets."""
    print("\n" + "=" * 70)
    print("TEST 2 & 4: _expert_best_category_v2 (all categories remaining)")
    print("=" * 70)

    scorecard = build_empty_scorecard()
    remaining = _remaining_categories(scorecard)

    cat_a = _expert_best_category_v2(DICE_A, remaining, scorecard)
    cat_b = _expert_best_category_v2(DICE_B, remaining, scorecard)
    print(f"[DICE_A] _expert_best_category_v2 => {cat_a!r}")
    print(f"[DICE_B] _expert_best_category_v2 => {cat_b!r}")

    # _expert_best_category_v2 should pick full_house for DICE_B because
    # it scores 25 which is the highest possible for [1,1,6,6,6].
    # (Checking that it's a reasonable choice, not strictly asserting
    #  because the bonus-aware logic could prefer something else if bonuses
    #  are at play -- but with an empty scorecard, full_house should win.)
    cat_b_score = score_for_category(DICE_B, cat_b)
    fh_score = score_for_category(DICE_B, 'full_house')
    print(f"  chosen category for DICE_B scores {cat_b_score} "
          f"(full_house = {fh_score})")

    # _expert_best_category_v2 should NOT pick a 0-scoring rare cat
    # for DICE_A since many categories score positive.
    cat_a_score = score_for_category(DICE_A, cat_a)
    print(f"  chosen category for DICE_A scores {cat_a_score}")

    print("PASS (no crash, values printed)")


def test_keep_candidates():
    """Test 5: examine _keep_candidates for [1, 2, 6, 4, 6]."""
    print("\n" + "=" * 70)
    print("TEST 5: _keep_candidates for [1, 2, 6, 4, 6] (roll-2 state)")
    print("=" * 70)

    masks = _keep_candidates(DICE_ROLL2)
    print(f"Number of keep candidates: {len(masks)}")
    for m in sorted(masks):
        kept_indices = [i for i in range(5) if (m >> i) & 1]
        kept_values = [DICE_ROLL2[i] for i in kept_indices]
        print(f"  mask {m:05b} (0b{m:05b}, {m:2d}) -> keep indices {kept_indices} "
              f"=> values {kept_values}")

    # Is index 3 (value 4) kept by any mask?  Index 3 corresponds to bit 3.
    # Mask 3 (0b00011) keeps indices {0,1} -> values [1,2]   -- NO
    # Mask 20 (0b10100) keeps indices {2,4} -> values [6,6]  -- NO
    # Mask 31 (0b11111) keeps all           -> includes index 3 -- YES
    mask_keeps_idx3 = [m for m in masks if (m >> 3) & 1]
    if mask_keeps_idx3:
        print(f"\n  => Index 3 (value 4) IS kept by mask(s): "
              f"{[f'{m:05b}' for m in mask_keeps_idx3]}")
    else:
        print(f"\n  => Index 3 (value 4) is NOT kept by any candidate mask")

    # The key question: can the player choose to keep the 4 (index 3)?
    # The keep-all mask (31) keeps everything. But the question is about
    # keeping ONLY specific dice. Let's check if there's a mask that
    # keeps index 3 without keeping all dice.
    non_all_masks = [m for m in masks if m != 0b11111 and ((m >> 3) & 1)]
    if non_all_masks:
        print(f"  => Index 3 can be kept selectively by mask(s): "
              f"{[f'{m:05b}' for m in non_all_masks]}")
    else:
        print(f"  => Index 3 cannot be kept selectively (only via keep-all) "
              f"by the candidate masks; the bot would reroll it.")


def test_full_house_specific():
    """Extra: verify full_house logic for known corner cases."""
    print("\n" + "=" * 70)
    print("EXTRA: full_house edge cases")
    print("=" * 70)

    cases = [
        ([1, 1, 1, 2, 2], 25, "trips + pair"),
        ([1, 1, 6, 4, 6], 0, "two pair"),
        ([1, 1, 6, 6, 6], 25, "trips + pair (same as DICE_B)"),
        ([1, 2, 3, 4, 5], 0, "straight, no pair"),
        ([1, 1, 1, 1, 2], 0, "four of a kind (not full house)"),
        ([1, 1, 1, 1, 1], 0, "five of a kind (not full house)"),
        ([1, 1, 2, 2, 2], 25, "trips + pair (unordered)"),
    ]
    all_pass = True
    for dice, expected, desc in cases:
        result = score_for_category(dice, 'full_house')
        ok = result == expected
        status = "PASS" if ok else "FAIL"
        if not ok:
            all_pass = False
        print(f"  {dice} -> full_house = {result:2d}  (expected {expected:2d})  "
              f"[{desc}] {status}")

    if all_pass:
        print("  All full_house edge cases PASS")
    else:
        print("  SOME full_house edge cases FAILED")


def main():
    print("=" * 70)
    print("Poker Dice Scoring Validation Test")
    print("=" * 70)

    # Tests 1 & 3: Score tables
    scores_a, scores_b = test_score_tables()

    # Tests 2 & 4: Bot category choosers
    test_bot_choose_category(scores_a, scores_b)
    test_expert_best_category_v2(scores_a, scores_b)

    # Test 5: Keep candidates
    test_keep_candidates()

    # Extra
    test_full_house_specific()

    # Summary
    print("\n" + "=" * 70)
    print("ALL TESTS COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()
