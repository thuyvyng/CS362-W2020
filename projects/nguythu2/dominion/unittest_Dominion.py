from unittest import TestCase
from collections import defaultdict
import testUtility
import Dominion


class TestCard(TestCase):
    def setUp(self):
        player_names = ["Annie", "*Ben", "*Carla"]
        nV = 12
        nC = 10 * len(player_names)

        self.box = testUtility.GetBoxes(nC)
        self.supply_order = testUtility.FillSupplyOrder()

        random10 = testUtility.PickTen(self.box)

        # Filling the supply
        self.supply = testUtility.FillSupply(player_names, nV, nC, self.box, random10)

        # initialize the trash
        self.trash = []

        # Costruct the Player objects
        self.players = testUtility.CreatePlayerObjects(player_names)
        self.player = Dominion.Player('Annie')

    def test_init(self):
        self.setUp()
        cost = 1
        buypower = 5

        card = Dominion.Coin_card(self.player.name, cost, buypower)

        self.assertEqual('Annie', card.name)

    def test_react(self):
        pass


class TestAction_card(TestCase):
    def setUp(self):

        self.trash = []
        self.player = Dominion.Player('Annie')
        self.testplayer = Dominion.Player('Annie')
        self.player.actions = 0
        self.testplayer.actions = 0
        self.player.buys = 0
        self.testplayer.buys = 0
        self.player.purse = 0
        self.testplayer.purse = 0
        self.name = "TestCard"
        self.cost = 3
        self.actions = 1
        self.cards = 1
        self.buys = 1
        self.coins = 9

    def test_init(self):
        self.setUp()
        testAction = Dominion.Action_card(self.name, self.cost, self.actions, self.cards, self.buys, self.coins)

        self.assertEqual(self.cost, testAction.cost)
        self.assertEqual('action', testAction.category)
        self.assertEqual(self.coins, testAction.coins)
        self.assertEqual(self.name, testAction.name)
        self.assertEqual(self.actions, testAction.actions)
        self.assertEqual(self.buys, testAction.buys)
        self.assertEqual(self.cards, testAction.cards)

        # i wasn't sure if we were supposed to see if inheritance works- someone said we would make a different unit test for this but i was unsure
        wood = Dominion.Woodcutter()

        # tests that smithy & wood are initialied correctly (checks cost, card category, and victory points)
        self.assertEqual(3, wood.cost)
        self.assertEqual('action', wood.category)
        self.assertEqual(0, wood.vpoints)

        smith = Dominion.Smithy()

        self.assertEqual(4, smith.cost)
        self.assertEqual('action', wood.category)
        self.assertEqual(0, smith.vpoints)

    def test_use(self):
        self.setUp()

        testActionCard = Dominion.Action_card(self.name, self.cost, self.actions, self.cards, self.buys, self.coins)

        self.player.hand.append(testActionCard)

        current_hand = len(self.player.hand)
        testActionCard.use(self.player, self.trash)

        self.assertEqual(len(self.testplayer.played) + 1, len(self.player.played))
        self.assertEqual(len(self.player.hand), current_hand - 1)

    def test_augment(self):
        self.setUp()

        testCard = Dominion.Action_card(self.name, self.cost, self.actions, self.cards, self.buys, self.coins)
        self.player.hand.append(testCard)
        testCard.augment(self.player)

        self.assertEqual(self.player.actions, self.testplayer.actions + testCard.actions)
        self.assertEqual(self.player.purse, self.testplayer.purse + testCard.coins)
        self.assertEqual(self.player.buys, self.testplayer.purse + testCard.buys)


class TestPlayer(TestCase):
    def setUp(self):
        self.player = Dominion.Player("Annie");
        self.before_player = Dominion.Player("Annie")
        self.before_player2 = Dominion.Player("Annie")

    def test_draw(self):
        self.setUp()

        self.player.draw()

        randomcard = Dominion.Silver()
        self.player.discard.append(randomcard)

        before_discard = self.player.discard
        before_discard.pop()

        self.assertEqual(len(self.player.hand), len(self.before_player.hand) + 1)

        if len(self.player.deck) == 0:
            self.assertEqual(len(self.player.deck), len(self.before_player.discard) - 1)
            self.assertEqual(len(self.player.discard), 0)
            self.assertEqual(len(before_discard), len(self.player.deck))
        else:
            self.assertEqual(len(self.player.deck), len(self.before_player.deck) - 1)

    def test_action_balance(self):
        self.setUp()

        # makes an action card that should also make action balance greater
        actionCard = Dominion.Action_card("Test", 1, 2, 1, 1, 1)
        coinCard = Dominion.Silver()
        actionCard2 = Dominion.Action_card("Test", 1, 1, 1, 1, 1)

        self.player.hand.append(actionCard)
        self.before_player.hand.append(coinCard)
        self.before_player2.hand.append(actionCard2)

        self.assertTrue(self.player.action_balance() > self.before_player.action_balance())
        self.assertEqual(self.before_player.action_balance(), self.before_player2.action_balance())

    def test_cardsummary(self):
        self.setUp()

        # print(len(self.player.deck + self.player.hand + self.player.played + self.player.discard + self.player.aside + self.player.hold))

        initialVPoints = self.player.cardsummary()['VICTORY POINTS']
        notVictoryCard = Dominion.Silver()
        VictoryCard = Dominion.Duchy()

        self.assertEqual(self.player.cardsummary()['VICTORY POINTS'], initialVPoints)
        self.player.hand.append(notVictoryCard)
        self.assertEqual(self.player.cardsummary()['VICTORY POINTS'], initialVPoints)
        self.player.hand.append(VictoryCard)
        self.assertEqual(self.player.cardsummary()['VICTORY POINTS'], initialVPoints + VictoryCard.vpoints)
        self.assertEqual(self.player.cardsummary()['Silver'], 1)

    def test_calcpoints(self):
        self.setUp()

        initialVPoints = self.player.cardsummary()['VICTORY POINTS']
        gardens = Dominion.Gardens()
        VictoryCard = Dominion.Duchy()

        self.player.hand.append(VictoryCard)

        self.assertEqual(self.player.calcpoints(), initialVPoints + VictoryCard.vpoints)
        self.assertTrue(self.player.calcpoints() > self.before_player.calcpoints())

        before_gardens = self.player.calcpoints()
        self.player.hand.append(gardens)
        self.assertTrue(self.player.calcpoints() > before_gardens)


class Test(TestCase):
    def setUp(self):
        self.supply = defaultdict(list)
        self.supply["Copper"] = [Dominion.Copper()] * (30)
        self.supply["Silver"] = [Dominion.Silver()] * 40
        self.supply["Gold"] = [Dominion.Gold()] * 30
        self.supply["Estate"] = [Dominion.Estate()] * 5
        self.supply["Duchy"] = [Dominion.Duchy()] * 5
        self.supply["Province"] = [Dominion.Province()] * 5
        self.supply["Curse"] = [Dominion.Curse()] * 5

    def test_gameover(self):
        self.setUp()
        self.assertEqual(Dominion.gameover(self.supply), False)

        self.supply["Province"] = []

        self.assertEqual(Dominion.gameover(self.supply), True)

        self.supply["Province"] = [Dominion.Province()] * 5

        self.supply["Copper"] = []

        self.assertEqual(Dominion.gameover(self.supply), False)
        self.supply["Silver"] = []
        self.assertEqual(Dominion.gameover(self.supply), False)
        self.supply["Gold"] = []
        self.assertEqual(Dominion.gameover(self.supply), True)



