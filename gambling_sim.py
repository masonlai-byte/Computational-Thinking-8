import random
import time
from itertools import combinations
from collections import Counter

RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
SUITS = ["♠", "♥", "♦", "♣"]
RANK_VALUE = {rank: value for value, rank in enumerate(RANKS, 2)}
RANK_VALUE["A"] = 14

STARTING_BANKROLL = 100
DEALER_STANDS_ON = 17

HAND_NAMES = {
    8: "Straight flush",
    7: "Four of a kind",
    6: "Full house",
    5: "Flush",
    4: "Straight",
    3: "Three of a kind",
    2: "Two pair",
    1: "One pair",
    0: "High card",
}

# ---------------------------------------------------------------- deck

class Deck:
    """A single 52-card deck that reshuffles itself when it runs out."""

    def __init__(self):
        self.cards = []
        self.reshuffle()

    def reshuffle(self):
        self.cards = [(rank, suit) for rank in RANKS for suit in SUITS]
        random.shuffle(self.cards)

    def draw(self):
        if not self.cards:
            self.reshuffle()
        return self.cards.pop()

    def __len__(self):
        return len(self.cards)

# ---------------------------------------------------------------- formatting

def new_deck():
    deck = [(rank, suit) for rank in RANKS for suit in SUITS]
    random.shuffle(deck)
    return deck

def format_card(card):
    rank, suit = card
    return f"{rank}{suit}"

def show_hand(cards):
    return " ".join(format_card(card) for card in cards)

def describe_total(cards):
    total = hand_total(cards)
    if total > 21:
        return f"bust with {total}"
    if is_soft(cards):
        return f"soft {total}"
    return f"{total}"

def describe_poker_hand(score):
    return HAND_NAMES.get(score[0], "Unknown")

# ---------------------------------------------------------------- statistics

class Stats:
    def __init__(self):
        self.rounds = 0
        self.wins = 0
        self.losses = 0
        self.pushes = 0
        self.biggest_win = 0
        self.spins = 0
        self.biggest_spin = 0

    def record(self, result, amount):
        self.rounds += 1
        if result == "win":
            self.wins += 1
            self.biggest_win = max(self.biggest_win, amount)
        elif result == "loss":
            self.losses += 1
        else:
            self.pushes += 1

    def record_spin(self, net):
        self.spins += 1
        if net > 0:
            self.biggest_spin = max(self.biggest_spin, net)

    def report(self):
        print(f"\nRounds played: {self.rounds}")
        print(f"  wins:   {self.wins}")
        print(f"  losses: {self.losses}")
        print(f"  pushes: {self.pushes}")
        print(f"  best single win: {self.biggest_win} credits")
        if self.spins:
            print(f"Slot spins: {self.spins}")
            print(f"  best spin: {self.biggest_spin} credits")

STATS = Stats()

# ---------------------------------------------------------------- betting

def get_bet(bankroll):
    while True:
        raw = input(f"Place your bet (1-{bankroll}, 'half', or 'all'): ").strip().lower()

        if raw in ("all", "max"):
            return bankroll
        if raw == "half":
            return max(1, bankroll // 2)

        try:
            bet = int(raw)
        except ValueError:
            print("Enter a whole number.")
            continue

        if 1 <= bet <= bankroll:
            return bet
        print(f"Bet must be between 1 and {bankroll}.")

# ---------------------------------------------------------------- blackjack math

def hand_total(cards):
    total = 0
    aces = 0
    for rank, _ in cards:
        if rank == "A":
            aces += 1
            total += 11
        elif rank in ("10", "J", "Q", "K"):
            total += 10
        else:
            total += int(rank)
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total

def is_soft(cards):
    """True when an ace is still counted as 11."""
    total = 0
    aces = 0
    for rank, _ in cards:
        if rank == "A":
            aces += 1
            total += 11
        elif rank in ("10", "J", "Q", "K"):
            total += 10
        else:
            total += int(rank)
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return aces > 0 and total <= 21

# ---------------------------------------------------------------- poker math

def score_five(cards):
    """Sortable score for exactly five cards."""
    ranks = sorted((RANK_VALUE[rank] for rank, _ in cards), reverse=True)
    counts = Counter(ranks)
    groups = sorted(counts.items(), key=lambda item: (item[1], item[0]), reverse=True)
    flush = len({suit for _, suit in cards}) == 1

    unique = sorted(set(ranks), reverse=True)
    if 14 in unique:
        unique.append(1)  # Ace can be low in A-2-3-4-5
    straight_high = next(
        (unique[i] for i in range(len(unique) - 4)
         if unique[i] - unique[i + 4] == 4),
        0,
    )

    if flush and straight_high:
        return (8, straight_high)
    if groups[0][1] == 4:
        return (7, groups[0][0], groups[1][0])
    if groups[0][1] == 3 and groups[1][1] == 2:
        return (6, groups[0][0], groups[1][0])
    if flush:
        return (5, *ranks)
    if straight_high:
        return (4, straight_high)
    if groups[0][1] == 3:
        triple = groups[0][0]
        kickers = sorted((r for r in ranks if r != triple), reverse=True)
        return (3, triple, *kickers)
    if groups[0][1] == 2 and groups[1][1] == 2:
        pairs = sorted((r for r, n in counts.items() if n == 2), reverse=True)
        kicker = max(r for r, n in counts.items() if n == 1)
        return (2, *pairs, kicker)
    if groups[0][1] == 2:
        pair = groups[0][0]
        kickers = sorted((r for r in ranks if r != pair), reverse=True)
        return (1, pair, *kickers)
    return (0, *ranks)

def poker_hand_value(cards):
    """Return (score, best five cards) for the best five-card poker hand."""
    best_score = None
    best_cards = None

    for hand in combinations(cards, 5):
        score = score_five(hand)
        if best_score is None or score > best_score:
            best_score = score
            best_cards = hand

    return best_score, best_cards

# ---------------------------------------------------------------- slots math

SLOT_SYMBOLS = ["🍒", "🍋", "🔔", "🍀", "💎", "7️⃣"]
SLOT_WEIGHTS = [30, 25, 20, 12, 8, 5]

# Payout multiplier for three of a kind, per symbol.
TRIPLE_PAYOUTS = {
    "🍒": 4,
    "🍋": 6,
    "🔔": 10,
    "🍀": 20,
    "💎": 40,
    "7️⃣": 100,
}

PAIR_PAYOUT = 2      # any two matching symbols returns 2x the bet
JACKPOT_SYMBOL = "7️⃣"

def spin_reels():
    """Return three weighted random symbols."""
    return random.choices(SLOT_SYMBOLS, weights=SLOT_WEIGHTS, k=3)

def slot_payout(reels, bet):
    """Return (payout, description) for a spin."""
    counts = Counter(reels)

    if len(counts) == 1:
        symbol = reels[0]
        multiplier = TRIPLE_PAYOUTS[symbol]
        return bet * multiplier, f"three {symbol} — pays {multiplier}x"

    if len(counts) == 2:
        symbol = max(counts, key=counts.get)
        return bet * PAIR_PAYOUT, f"a pair of {symbol} — pays {PAIR_PAYOUT}x"

    return 0, "no match"

def show_reels(reels, spins=6, delay=0.12):
    """Print a short spinning animation, then the final reels."""
    for _ in range(spins):
        filler = random.choices(SLOT_SYMBOLS, weights=SLOT_WEIGHTS, k=3)
        print("\r  " + " | ".join(filler) + "  ", end="", flush=True)
        time.sleep(delay)
    print("\r  " + " | ".join(reels) + "  ")

# ---------------------------------------------------------------- blackjack

def play_blackjack(bankroll):
    bet = get_bet(bankroll)
    deck = Deck()
    player = [deck.draw(), deck.draw()]
    dealer = [deck.draw(), deck.draw()]

    print(f"\nYour cards: {show_hand(player)} ({describe_total(player)})")
    print(f"Dealer shows: {show_hand(dealer[:1])}")

    player_natural = hand_total(player) == 21
    dealer_natural = hand_total(dealer) == 21

    # Naturals resolve immediately.
    if player_natural or dealer_natural:
        print(f"Dealer's cards: {show_hand(dealer)} ({describe_total(dealer)})")
        if player_natural and dealer_natural:
            print("Both have blackjack — push.")
            STATS.record("push", 0)
            return bankroll
        if player_natural:
            winnings = bet * 3 // 2
            print(f"Blackjack! You win {winnings} credits.")
            STATS.record("win", winnings)
            return bankroll + winnings
        print("Dealer has blackjack.")
        STATS.record("loss", bet)
        return bankroll - bet

    # Player's turn.
    while True:
        total = hand_total(player)

        if total > 21:
            print("Bust! Dealer wins.")
            STATS.record("loss", bet)
            return bankroll - bet
        if total == 21:
            print("You have 21 — standing automatically.")
            break

        can_double = len(player) == 2 and bet * 2 <= bankroll
        prompt = "Hit or stand [h/s]"
        if can_double:
            prompt += ", double down [d]"

        action = input(prompt + ": ").strip().lower()

        if action in ("h", "hit"):
            player.append(deck.draw())
            print(f"You draw {show_hand(player[-1:])}. {describe_total(player)}")
        elif action in ("s", "stand"):
            break
        elif action in ("d", "double") and can_double:
            bet *= 2
            player.append(deck.draw())
            print(f"Double down! You draw {show_hand(player[-1:])}. {describe_total(player)}")
            if hand_total(player) > 21:
                print("Bust! Dealer wins.")
                STATS.record("loss", bet)
                return bankroll - bet
            break
        else:
            print("Enter h, s, or d.")

    # Dealer's turn.
    print(f"\nDealer's cards: {show_hand(dealer)} ({describe_total(dealer)})")
    while hand_total(dealer) < DEALER_STANDS_ON:
        dealer.append(deck.draw())
        print(f"Dealer draws {show_hand(dealer[-1:])}. {describe_total(dealer)}")

    player_total = hand_total(player)
    dealer_total = hand_total(dealer)

    if dealer_total > 21:
        print(f"Dealer busts with {dealer_total}. You win {bet} credits!")
        STATS.record("win", bet)
        return bankroll + bet
    if player_total > dealer_total:
        print(f"{player_total} beats {dealer_total}. You win {bet} credits!")
        STATS.record("win", bet)
        return bankroll + bet
    if player_total < dealer_total:
        print(f"{dealer_total} beats {player_total}. Dealer wins.")
        STATS.record("loss", bet)
        return bankroll - bet

    print(f"Both have {player_total} — push, your bet is returned.")
    STATS.record("push", 0)
    return bankroll

# ---------------------------------------------------------------- hold'em

def play_holdem(bankroll):
    bet = get_bet(bankroll)
    deck = Deck()
    player = [deck.draw(), deck.draw()]
    dealer = [deck.draw(), deck.draw()]
    board = [deck.draw() for _ in range(5)]

    print(f"\nYour cards: {show_hand(player)}")
    print(f"Dealer's cards: {show_hand(dealer)}")
    print(f"Community cards: {show_hand(board)}")

    player_score, player_best = poker_hand_value(player + board)
    dealer_score, dealer_best = poker_hand_value(dealer + board)

    print(f"You:    {describe_poker_hand(player_score)} ({show_hand(player_best)})")
    print(f"Dealer: {describe_poker_hand(dealer_score)} ({show_hand(dealer_best)})")

    if player_score > dealer_score:
        print(f"You win {bet} credits!")
        STATS.record("win", bet)
        return bankroll + bet
    if player_score < dealer_score:
        print("Dealer wins.")
        STATS.record("loss", bet)
        return bankroll - bet

    print("Tie — your bet is returned.")
    STATS.record("push", 0)
    return bankroll

# ---------------------------------------------------------------- slots

def play_slots(bankroll):
    print("\nSlot machine — three reels, match two to win, three to win big.")
    print("Payouts (three of a kind): "
          + ", ".join(f"{sym} {mult}x" for sym, mult in TRIPLE_PAYOUTS.items()))
    print(f"Any pair pays {PAIR_PAYOUT}x your bet.")

    bet = get_bet(bankroll)
    reels = spin_reels()

    print("\nSpinning...")
    show_reels(reels)

    payout, description = slot_payout(reels, bet)
    net = payout - bet

    print(f"Result: {description}.")

    if payout == 0:
        print(f"You lose {bet} credits.")
    elif net > 0:
        print(f"You win {net} credits!")
    elif net == 0:
        print("Break even — your bet is returned.")
    else:
        print(f"You lose {-net} credits.")

    if reels.count(JACKPOT_SYMBOL) == 3:
        print("*** JACKPOT! Triple sevens! ***")

    STATS.record_spin(net)

    if net > 0:
        STATS.record("win", net)
    elif net < 0:
        STATS.record("loss", -net)
    else:
        STATS.record("push", 0)

    return bankroll - bet + payout

# ---------------------------------------------------------------- main

def main():
    bankroll = STARTING_BANKROLL
    print("Card games — virtual credits only, no real money.")
    print("Menu: [b] Blackjack, [t] Texas Hold'em, [l] Slots, [s] stats, [q] quit")

    while bankroll > 0:
        print(f"\nBankroll: {bankroll} credits")
        game = input("Choose a game: ").strip().lower()

        if game in ("q", "quit"):
            break
        if game in ("s", "stats"):
            STATS.report()
            continue
        if game in ("b", "blackjack"):
            bankroll = play_blackjack(bankroll)
        elif game in ("t", "texas hold'em", "holdem", "poker"):
            bankroll = play_holdem(bankroll)
        elif game in ("l", "slots", "slot", "machine"):
            bankroll = play_slots(bankroll)
        else:
            print("Enter b, t, l, s, or q.")
            continue

        if bankroll > 0 and input("Play another round? [y/n]: ").strip().lower() != "y":
            break

    print(f"\nGame over. Final bankroll: {bankroll} credits.")
    STATS.report()

if __name__ == "__main__":
    main()

