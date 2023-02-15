#modification I want to change: 
#turning the src in a single code DONE
#adding the special wild card since the SRC isn't 
#According  to the rule decreasing the number of +4 cards cause there are only 4 DONE
#making the player 2 instead of 3 DONE


import random
from enum import Enum
import tkinter as tk
from tkinter import messagebox



class Card:
    def __init__(self, number, colour):
        self._number = number
        self._colour = colour
        self._amount = 0

    def get_number(self):
        return self._number

    def set_number(self, number):
        self._number = number

    def get_colour(self):
        return self._colour

    def set_colour(self, colour):
        self._colour = colour
    
    def get_pickup_amount(self):
        return self._amount

    def matches(self, card):
        if isinstance(card, Pickup4Card): #When starting game with special cards
            return True
        if self._colour == card.get_colour() or self._number == card.get_number():
            return True
        return False

    def play(self, player, game):
        return 0


class SkipCard(Card):
    def __init__(self, number, colour):
        Card.__init__(self, number, colour)
        
    def play(self, player, game):
        game.skip()


class ReverseCard(Card):
    def __init__(self, number, colour):
        Card.__init__(self, number, colour)

    def play(self, player, game):
        game.reverse()


class Pickup2Card(Card):
    def __init__(self, number, colour):
        Card.__init__(self, number, colour)
        self._amount = 2
    
    def get_pickup_amount(self):
        return self._amount

    def play(self, player, game):
        cards = game.pickup_pile.pick(self._amount)
        game.next_player().get_deck().add_cards(cards)
        game._turns._location = game._turns._location-1


class Pickup4Card(Card):
    def __init__(self, number, colour):
        Card.__init__(self, number, colour)
        self._amount = 4
    
    def get_pickup_amount(self):
        return self._amount

    def matches(self, putdown_pile):
        return True

    def play(self, player, game):
        cards = game.pickup_pile.pick(self._amount)
        game.next_player().get_deck().add_cards(cards)
        game._turns._location = game._turns._location-1

class WildCard(Card):
    def __init__(self, number, colour):
        Card.__init__(self, number, colour)
        self._amount = 0
    
    def get_pickup_amount(self):
        return self._amount
    
    def play(self, player, game):
        game.wild()
    

class Deck:
    def __init__(self, starting_cards = None):
        if starting_cards == None:
            self._cards = [] #DSA empty list
        else:
            self._cards = [] #DSA empty list
            self._cards.extend(starting_cards) #DSA List Methods & Built-In FunctIons extend()
 
    def get_cards(self):
        return self._cards
    
    def get_amount(self):
        return len(self._cards) #DSA using List Methods & Built-In FunctIons len ()

    def shuffle(self):
        random.shuffle(self._cards)

    def pick(self, amount = 1):
        picked_cards = [] #DSA empty list
        for i in range(0, amount):
            picked_cards.append(self._cards[i]) #DSA using List Methods & Built-In FunctIons append ()
        for i in range(0, amount):
            del self._cards[i]
        return picked_cards

    def add_card(self, card):
        self._cards.append(card) #DSA using List Methods & Built-In FunctIons append ()

    def add_cards(self, cards):
        self._cards.extend(cards) #DSA List Methods & Built-In FunctIons extend()

    def top(self):
        if len(self._cards) == 0:
            return None
        else:
            return self._cards[len(self._cards)-1] #DSA using List Methods & Built-In FunctIons len ()


class Player:
    def __init__(self, name):
        self._name = name
        self._deck = Deck()

    def get_name(self):
        return self._name
    
    def get_deck(self):
        return self._deck

    def is_playable(self):
        raise NotImplementedError("is_playable to be implemented by subclasses")
    
    def has_won(self):
        if self._deck.get_amount() == 0:
            return True
        else:
            return False

    def pick_card(self, putdown_pile):
        raise NotImplementedError("pick_card to be implemented by subclasses")


class HumanPlayer(Player):
    def __init__(self, name):
        Player.__init__(self, name)
        self._deck = Deck()

    def is_playable(self):
        return True

    def pick_card(self, putdown_pile):
        return None


class ComputerPlayer(Player):
    def __init__(self, name):
        Player.__init__(self, name)
        self._deck = Deck()

    def is_playable(self):
        return False

    def pick_card(self, putdown_pile): #BUG, Computer player can't activate Pick4Card effect
        for i in self._deck.get_cards():
            if i.matches(putdown_pile.top()):
                picked_card = i
                self._deck.get_cards().remove(i)
                return picked_card
        return None

class CardColour(Enum):
    """
    An enumeration of card colours in the Uno game.
    """
    blue = "#508ebf"
    red = "#a30e15"
    yellow = "#f9bf3b"
    green = "#5d8402"
    black = "#222"


FULL_DECK = [
    (Card(0, CardColour.red), (0, 10)),
    (Card(0, CardColour.yellow), (0, 10)),
    (Card(0, CardColour.green), (0, 10)),
    (Card(0, CardColour.blue), (0, 10)),
    (Card(0, CardColour.red), (1, 10)),
    (Card(0, CardColour.yellow), (1, 10)),
    (Card(0, CardColour.green), (1, 10)),
    (Card(0, CardColour.blue), (1, 10)),

    (SkipCard(0, CardColour.red), (0, 2)),
    (SkipCard(0, CardColour.yellow), (0, 2)),
    (SkipCard(0, CardColour.green), (0, 2)),
    (SkipCard(0, CardColour.blue), (0, 2)),

    (ReverseCard(0, CardColour.red), (0, 2)),
    (ReverseCard(0, CardColour.yellow), (0, 2)),
    (ReverseCard(0, CardColour.green), (0, 2)),
    (ReverseCard(0, CardColour.blue), (0, 2)),

    (Pickup2Card(0, CardColour.red), (0, 2)),
    (Pickup2Card(0, CardColour.yellow), (0, 2)),
    (Pickup2Card(0, CardColour.green), (0, 2)),
    (Pickup2Card(0, CardColour.blue), (0, 2)),

    (Pickup4Card(0, CardColour.black), (0, 2)),
    (Pickup4Card(0, CardColour.black), (0, 2)),

    (WildCard(0, CardColour.black), (0, 2)),
    (WildCard(0, CardColour.black), (0, 2)),
]
##adding List 


SPECIAL_CARDS = [Pickup4Card]


class TurnManager:
    """
    A class to manage the order of turns amongst game players.
    """
    def __init__(self, players):
        """
        Construct a new turn manager to based on game players.
        Parameters:
             players (list<T>): An ordered list of players to store.
        """
        self._players = players
        # start in correct direction
        self._direction = True
        self._location = 0
        self._max = len(players) #DSA using List Methods & Built-In FunctIons len ()

    def current(self):
        """
        (T) Returns the player whose turn it is.
        """
        return self._players[self._location]

    def next(self):
        """
        (T) Moves onto the next players turn and return that player.
        """
        return self.skip(count=0)

    def peak(self, count=1):
        """
        Look forward or backwards in the current ordering of turns.
        Parameters:
            count (int): The amount of turns to look forward,
                         if negative, looks backwards.
        Returns:
            (T): The player we are peaking at.
        """
        location = self._location
        location += count if self._direction else -count
        location %= self._max
        return self._players[location]

    def reverse(self):
        """
        Reverse the order of turns.
        """
        self._direction = not self._direction

    def skip(self, count=0):
        """
        (T): Moves onto the next player, skipping 'count' amount players.
        """
        count += 1
        self._location += count if self._direction else -count
        self._location %= self._max
        return self._players[self._location]
    
    def wild (self, count=0):
        count += 1
        self._location += count if self._direction else -count
        self._location %= self._max
        return self._players[self._location]


class UnoGame:
    """
    A game of Uno++.
    """
    def __init__(self, deck, players):
        """
        Construct a game of uno from a pickup pile and list of players.
        Parameters:
            deck (Deck): The pile of cards to pickup from.
            players (list<Player>): The players in this game of uno.
        """
        self.pickup_pile = deck
        self.players = players

        self._turns = TurnManager(players)

        self.putdown_pile = Deck(self.pickup_pile.pick())
        self.special_pile = Deck()

        self._is_over = False
        self.winner = None

    def next_player(self):
        """
        Changes to the next player in the game and returns an instance of them.
        Returns:
            (Player): The next player in the game.
        """
        return self._turns.next() #DSA List Methods & Built-In FunctIons next()
    def current_player(self):
        """
        (Player) Returns the player whose turn it is currently.
        """
        return self._turns.current()#DSA List Methods & Built-In FunctIons current ()

    def skip(self):
        """Prevent the next player from taking their turn."""
        self._turns.skip() #DSA List Methods & Built-In FunctIons skip ()
    
    def wild(self):
        """Prevent the next player from taking their turn."""
        self._turns.skip()

    def reverse(self):
        """Transfer the turn back to the previous player and reverse the order."""
        self._turns.reverse() #DSA List Methods & Built-In FunctIons reverse()

    def get_turns(self):
        """(TurnManager) Returns the turn manager for this game."""
        return self._turns

    def is_over(self):
        """
        (bool): True iff the game has been won. Assigns the winner variable.
        """
        for player in self.players:
            if player.has_won():
                self.winner = player
                self._is_over = True

        return self._is_over

    def select_card(self, player, card):
        """Perform actions for a player selecting a card
        Parameters:
            player (Player): The selecting player.
            card (Card): The card to select.
        """
        card.play(player, self)
        if card.__class__ in SPECIAL_CARDS:
            self.special_pile.add_card(card)
        else:
            self.putdown_pile.add_card(card)

    def take_turn(self, player):
        """
        Takes the turn of the given player by having them select a card.
        Parameters:
            player (Player): The player whose turn it is.
        """
        card = player.pick_card(self.putdown_pile)

        if card is None:
            player.get_deck().add_cards(self.pickup_pile.pick())
            return

        if card.matches(self.putdown_pile.top()):
            self.select_card(player, card)

    def take_turns(self):
        """
        Plays an entire round by taking the turn for each player in the game.
        """
        for player in self.players:
            self.take_turn(player)

            if player.has_won():
                return


def build_deck(structure, range_cards=(Card, )):
    """
    Construct a deck from a simplified deck structure.
    Example structure:
    [ (Card(colour=CardColour.red), (0, 10)),
      (SkipCard(colour=CardColour.green), (3, 5)) ]
    Creates a deck with red cards numbered from 0 up to but not including 10 and
    skip cards with the numbers 3 and 4. Assuming both cards are in range_cards,
    otherwise creates the same amount of cards with -1 as their numbers.
    Parameters:
        structure (list<tuple>): The simplified deck structure.
        range_cards (tuple<Card>): Cards whose numbers should be updated from -1.
    """
    deck = [] #empty list

    for (card, (start, end)) in structure:
        for number in range(start, end):
            new_card = card.__class__(-1, card.get_colour())
            if card.__class__ in range_cards:
                new_card.set_number(number)
            deck.append(new_card)

    return deck




CARD_HEIGHT = 100
CARD_WIDTH = 75
CARD_SPACE = 10

CARD_OVAL_COLOUR = "#fceee3"
CARD_BACK_BACKGROUND = "black"
CARD_BACK_FOREGROUND = "red"
CARD_BACK_TEXT_COLOUR = "yellow"
CARD_BACK_TEXT = "UNO"

AI_DELAY = 2000


class CardView:
    """
    A class to manage the drawing of a Uno card on a canvas.
    """

    def __init__(self, canvas, left_side, oval_colour=CARD_OVAL_COLOUR,
                 background_colour=CARD_BACK_BACKGROUND,
                 foreground_colour=CARD_BACK_FOREGROUND,
                 text_colour=CARD_BACK_TEXT_COLOUR, text=CARD_BACK_TEXT):
        """
        Construct a new card to be drawn on the given canvas at the left_position.
        Parameters:
            canvas (tk.Canvas): The canvas to draw the card onto.
            left_side (int): The amount of pixels in the canvas to draw the card.
            oval_colour (tk.Color): Colour of the oval for this card.
            background_colour (tk.Color): Backface card background colour.
            foreground_colour (tk.Color): Backface card foreground colour.
            text_colour (tk.Color): Backface card text colour.
            text (str): Backface card text to display.
        """
        self._canvas = canvas

        self.left_side = left_side
        self.right_side = left_side + CARD_WIDTH

        self._oval_colour = oval_colour
        self._background = background_colour
        self._foreground = foreground_colour
        self._text_colour = text_colour
        self._text = text
        self._image = None

        self.draw()

    def draw(self):
        """Draw the backface of the card to the canvas."""
        self._back = self.draw_back(self._background)
        self._oval = self.draw_circle(self._foreground)
        self._text_view = self.draw_text(self._text, self._text_colour)

    def redraw(self, card):
        """Redraw the card view with the properties of the given card.
        Parameters:
            card (Card): The card to draw to the canvas. If None, draw the
                         backface of the card.
        """
        if card is not None:
            # draw the card with details from the card parameter
            self._canvas.itemconfig(self._back, fill=card.get_colour().value)
            self._canvas.itemconfig(self._oval, fill=self._oval_colour)
            self._canvas.itemconfig(self._text_view, fill=card.get_colour().value,
                                    text=card.get_number())
        else:
            # draw the backface of the card
            self._canvas.itemconfig(self._back, fill=self._background)
            self._canvas.itemconfig(self._oval, fill=self._foreground)
            self._canvas.itemconfig(self._text_view, fill=self._text_colour,
                                    text=self._text)

    def draw_back(self, colour):
        """Draw the back of the canvas (the background not the backface).
        Parameters:
            colour (tk.Color): The colour of the background.
        """
        return self._canvas.create_rectangle(self.left_side, 0,
                                             self.right_side, CARD_HEIGHT,
                                             fill=colour)

    def draw_circle(self, colour):
        """Draw a circle in the middle of the card.
        Parameters:
            colour (tk.Color): The colour of the cirlce.
        """
        return self._canvas.create_oval(self.left_side + 10, 10,
                                        self.right_side - 10, CARD_HEIGHT - 10,
                                        fill=colour)

    def draw_text(self, text, colour):
        """Draw text in the middle of the card.
        Parameters:
            text (str): The text to display on the card.
            colour (tk.Color): The colour of the text to display.
        """
        return self._canvas.create_text(self.left_side + (CARD_WIDTH // 2),
                                        CARD_HEIGHT // 2, text=text, fill=colour,
                                        font=('Times', '16', 'bold italic'))

    def draw_image(self, image):
        """Draw an image in the middle of the card.
        Parameters:
            image (str): The filepath of the image to display.
        """
        self._image = tk.PhotoImage(file=image)
        return self._canvas.create_image(self.left_side + (CARD_WIDTH // 2),
                                         CARD_HEIGHT // 2, image=self._image)


CARD_ICONS = {
    SkipCard: "skip",
    ReverseCard: "reverse",
    WildCard: "wild"
}
##dictionary

class IconCardView(CardView):
    """
    A card that has an image associated with it.
    """

    def draw(self):
        """Draw the backface of the card to the canvas."""
        super().draw()
        self._image_view = None

    def redraw(self, card):
        """Redraw the card view with an icon.
        Parameters:
            card (Card): The card to draw to the canvas. If None, draw the
                         backface of the card.
        """
        super().redraw(card)

        if card is not None:
            # clear text on the card
            self._canvas.itemconfig(self._text_view, text="")

            if self._image_view is None:
                # draw an image based on the card's class
                image = CARD_ICONS.get(card.__class__, "skip")
                self._image_view = self.draw_image(f"images/{image}.png")
            else:
                # show the image
                self._canvas.itemconfig(self._image_view, state="normal")
        else:
            if self._image_view is not None:
                # hide the image
                self._canvas.itemconfig(self._image_view, state="hidden")


class PickupCardView(CardView):
    """
    A card that displays the amount of cards to pickup.
    """

    def redraw(self, card):
        """Redraw the card view with the properties of the given card.
        Parameters:
            card (Card): The card to draw to the canvas. If None, draw the
                         backface of the card.
        """
        super().redraw(card)

        if card is not None:
            self._canvas.itemconfig(self._text_view,
                                    text=f"+{card.get_pickup_amount()}")

class wildCardView(CardView):
    """
    A card that has an image associated with it.
    """

    def draw(self):
        """Draw the backface of the card to the canvas."""
        super().draw()
        self._image_view = None

    def redraw(self, card):
        """Redraw the card view with an icon.
        Parameters:
            card (Card): The card to draw to the canvas. If None, draw the
                         backface of the card.
        """
        super().redraw(card)

        if card is not None:
            # clear text on the card
            self._canvas.itemconfig(self._text_view, text="")

            if self._image_view is None:
                # draw an image based on the card's class
                image = CARD_ICONS.get(card.__class__, "reverse")
                self._image_view = self.draw_image(f"images/{image}.png")
            else:
                # show the image
                self._canvas.itemconfig(self._image_view, state="normal")
        else:
            if self._image_view is not None:
                # hide the image
                self._canvas.itemconfig(self._image_view, state="hidden")



CARD_VIEWS = {
    SkipCard: IconCardView,
    ReverseCard: IconCardView,
    Pickup2Card: PickupCardView,
    Pickup4Card: PickupCardView,
    WildCard: wildCardView
}


class DeckView(tk.Canvas):
    """
    A Canvas that displays a deck of uno cards on a board.
    """

    def __init__(self, master, pick_card=None, border_colour="#6D4C41",
                 active_border="red", offset=CARD_WIDTH, *args, **kwargs):
        """
        Construct a deck view.
        Parameters:
            master (tk.Tk|tk.Frame): The parent of this canvas.
            pick_card (callable): The callback when card in this deck is clicked.
                                  Takes an int representing the cards index.
            border_colour (tk.Color): The colour of the decks border.
            offset (int): The offset between cards in the deck.
        """
        super().__init__(master, *args, **kwargs, bg=border_colour,
                         highlightthickness=5, highlightbackground=border_colour)

        self._active = False
        self._playing = False

        self.offset = offset
        self.pick_card = pick_card
        self.cards = {} #DSA dictionary

        self._border_colour = border_colour
        self._active_border = active_border

        self.bind("<Button-1>", self._handle_click)

    def toggle_active(self, active=None):
        """Toggle whether the deck should be clickable.
        Parameters:
            active (bool): Whether to activate the deck.
        """
        if active is None:
            self._active = not self._active
        else:
            self._active = active

    def toggle_playing(self, playing=None):
        """Toggle whether the deck is the deck being played.
        Parameters:
            playing (bool): Whether this deck is being played.
        """
        if playing is None:
            self._playing = not self._active
        else:
            self._playing = playing

    def _handle_click(self, event):
        """Handles when the player clicks the deck."""
        # the index of the card in the deck
        slot = event.x // CARD_WIDTH

        if self.pick_card is not None and self._active:
            self.pick_card(slot)

    def get_card_view(self, card):
        """Determines the view class for a card.
        Parameters:
            card (Card): The card that requires a view.
        Returns:
            (CardView): The view for the given card.
        """
        return CARD_VIEWS.get(card.__class__, CardView)

    def draw_card(self, card, slot):
        """
        Draw a card in the given slot on the deck.
        Parameters:
            card (Card): The card to draw to the deck.
            slot (int): The position in the deck to draw the card.
        Returns:
            (CardView): The card view drawn at the slot for a given card.
        """
        left_side = slot * self.offset

        view = self.get_card_view(card)
        self.cards[slot] = view(self, left_side)

        return self.cards[slot]

    def draw(self, deck, show=True):
        """
        Draw the deck based of the data in a given deck instance.
        Parameter:
            deck (Deck): The deck to draw in this canvas.
            show (bool): Whether the cards should be displayed or not.
        """
        # resize the canvas to fit all the cards in the deck
        self.resize(deck.get_amount())

        # highlight border
        if self._playing:
            self.config(highlightbackground=self._active_border)
        else:
            self.config(highlightbackground=self._border_colour)

        for i, card in enumerate(deck.get_cards()):

            # retrieve the CardView class for this card
            view = self.cards.get(i, None)

            # draw the CardView if it doesn't exist already
            if view is None:
                view = self.draw_card(card, i)

            # if the type of card has changed, redraw the CardView
            if type(view) != self.get_card_view(card):
                view = self.draw_card(card, i)

            # update details in the CardView
            view.redraw(card if show else None)

    def resize(self, size):
        """
        Calculate the dimensions required to fit 'size' cards in this canvas
        and update the canvas size.
        Parameters:
            size (int): The amount of cards that should be displayed in this deck.
        """
        # ensure that the deck is at least one card wide
        if self.offset < CARD_WIDTH:
            width = (self.offset * size) + CARD_WIDTH
        else:
            width = (self.offset * size)

        height = CARD_HEIGHT

        # resize canvas, adjust for border
        self.config(width=width - 10, height=height - 10)


class UnoApp:
    """A graphical Uno application"""

    def __init__(self, master, game, board_colour="#F9B05A"):
        """Create a new Uno application based on a given UnoGame.
        Parameters:
            master (tk.Tk): The root window for the Uno application.
            game (UnoGame): The game to display in this application.
            board_colour (tk.Color): The background colour of the board.
        """
        self._master = master
        self.game = game
        self.board_colour = board_colour

        # define all the class variables
        self._board = self.decks = self._putdown_pile = self._pickup_pile \
            = self._special_pile = None

        self.render_decks()

        self.add_menu()

    def render_decks(self):
        # remove old frame, if it exists
        if self._board is not None:
            self._board.pack_forget()

        # create a board frame
        self._board = board = tk.Frame(self._master, padx=20, pady=20,
                                       bg=self.board_colour,
                                       borderwidth=2, relief="groove")
        board.pack(expand=True, fill=tk.BOTH)

        self.decks = decks = {} #DSA Dictionary

        # split the board evenly
        split = len(self.game.players) // 2

        # draw the first decks of players
        for i, player in enumerate(self.game.players[:split]):
            decks[player] = self.draw_deck(player, show=False)
            self.draw_title(player)

        # draw the middle row of piles
        self._putdown_pile, self._pickup_pile, self._special_pile = self.draw_board()

        # draw the second decks of players
        for i, player in enumerate(self.game.players[split:]):
            decks[player] = self.draw_deck(player, show=False)
            self.draw_title(player)

    def update(self):
        """Redraw all the decks in the game."""
        # draw all player decks
        for player in self.game.players:
            playing = player == self.game.current_player()
            clickable = player.is_playable() and playing
            self.decks[player].toggle_active(active=clickable)
            self.decks[player].toggle_playing(playing=playing)
            self.decks[player].draw(player.get_deck(), show=clickable)

        # draw the pile decks
        self._putdown_pile.draw(self.game.putdown_pile)
        self._pickup_pile.draw(self.game.pickup_pile, show=False)
        self._special_pile.draw(self.game.special_pile)

    def new_game(self):
        """Start a new game"""
        # clone the old players
        players = [] #DSA LIST
        for player in self.game.players:
            players.append(player.__class__(player.get_name()))

        # generate a new deck
        pickup_pile = Deck(build_deck(FULL_DECK))
        pickup_pile.shuffle()

        # make players pickup cards
        for player in players:
            cards = pickup_pile.pick(7)
            player.get_deck().add_cards(cards)

        self.game = UnoGame(pickup_pile, players)
        self.render_decks()
        self.update()

    def add_menu(self):
        """Create a menu for the application"""
        menu = tk.Menu(self._master)

        # file menu with new game and exit
        file = tk.Menu(menu)
        file.add_command(label="New Game", command=self.new_game)
        file.add_command(label="Exit", command=self._master.destroy)

        # add file menu to menu
        menu.add_cascade(label="File", menu=file)
        self._master.config(menu=menu)

    def pick_card(self, player, slot):
        """Called when a given playable player selects a slot.
        Parameters:
            player (Player): The selecting player.
            slot (int): The card index they selected to play.
        """
        # get the selected card
        card = player.get_deck().get_cards()[slot]

        # pick the card if it matches
        if card.matches(self.game.putdown_pile.top()):
            card = player.get_deck().get_cards().pop(slot)
            self.game.select_card(player, card)

            # wait for next move
            self.step()

    def draw_card(self, _):
        """Pick up a card from the deck for the current player."""
        if not self.game.current_player().is_playable():
            return

        # select card from deck
        next_card = self.game.pickup_pile.pick()
        # add card to players deck
        self.game.current_player().get_deck().add_cards(next_card)

        # wait for next move
        self.step()

    def draw_board(self):
        """Draw the middle row of card piles to the board.
        Returns:
            tuple<DeckView, DeckView, DeckView>: The putdown, pickup and special
                                                 piles respectively.
        """
        board = tk.Frame(self._board, bg="#6D4C41")
        board.pack(side=tk.TOP, pady=20, fill=tk.X, expand=True)

        # left pickup card pile view
        pickup_pile = DeckView(board, offset=0, pick_card=self.draw_card)
        pickup_pile.toggle_active(active=True)
        pickup_pile.draw(self.game.putdown_pile, show=False)
        pickup_pile.pack(side=tk.LEFT, padx=50)

        # right putdown card pile view
        putdown_pile = DeckView(board, offset=2)
        putdown_pile.draw(self.game.putdown_pile)
        putdown_pile.pack(side=tk.RIGHT, padx=50)

        # middle right view for special cards
        special_pile = DeckView(board, offset=0)
        special_pile.draw(self.game.special_pile, show=False)
        special_pile.pack(side=tk.RIGHT)

        return putdown_pile, pickup_pile, special_pile

    def draw_deck(self, player, show=True):
        """Draw a players deck to the board
        Parameters:
            player (Player): The player whose deck should be drawn.
            show (bool): Whether or not to display the players deck.
        Returns:
            DeckView: The deck view for the player.
        """
        deck = DeckView(self._board,
                        pick_card=lambda card: self.pick_card(player, card))
        deck.pack(side=tk.TOP)
        deck.draw(player.get_deck(), show=show)
        return deck

    def draw_title(self, player):
        """Draw a deck label for a player to the board.
        Parameters:
            player (Player): The player to draw.
        """
        label = tk.Label(self._board, text=player.get_name(),
                         font=('Times', '24', 'bold italic'),
                         bg=self.board_colour)
        label.pack(side=tk.TOP)

    def step(self):
        """Perform actions to advance the game a turn."""
        # end the game if a player has won
        if self.game.is_over():
            messagebox.showinfo("Game Over",
                                f"{self.game.winner.get_name()} has won!")
            self._master.destroy()
            return

        # move to the next player
        player = self.game.next_player()
        self.update()

        # exit and wait for the player to make their move
        if player.is_playable():
            return

        self._master.after(AI_DELAY, self.take_turn)

    def take_turn(self):
        """Make an automated turn"""
        # make an automated move
        player = self.game.current_player()
        self.game.take_turn(player)
        self.update()

        self.step()

    def play(self):
        """Start the game running"""
        self.step()


def main():
    # create window for uno
    root = tk.Tk()
    root.title("Uno++")

    # build a list of players for the game
    players = [HumanPlayer("YOU"), ComputerPlayer("PLAYER 2")]

    # build a pickup pile
    pickup_pile = Deck(build_deck(FULL_DECK))
    pickup_pile.shuffle()

    # deal players cards from the pickup pile
    for player in players:
        cards = pickup_pile.pick(7)
        player.get_deck().add_cards(cards)

    # create and play the game
    game = UnoGame(pickup_pile, players)
    app = UnoApp(root, game)
    app.play()

    # update window dimensions
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    root.mainloop()


if __name__ == "__main__":
    main()
