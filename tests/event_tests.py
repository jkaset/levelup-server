import json
from rest_framework import status
from rest_framework.test import APITestCase
from levelupapi.models import Game_Type, Gamer, Game, Event


class EventTests(APITestCase):
    def setUp(self):
        """
        Create a new account and create sample category
        """
        url = "/register"
        data = {
            "username": "steve",
            "password": "Admin8*",
            "email": "steve@stevebrownlee.com",
            "address": "100 Infinity Way",
            "phone_number": "555-1212",
            "first_name": "Steve",
            "last_name": "Brownlee",
            "bio": "Love those gamez!!"
        }

        #game, schedular, gametype
        # Initiate request and capture response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Store the auth token
        self.token = json_response["token"]

        # Assert that a user was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # SEED DATABASE WITH ONE GAME TYPE
        # This is needed because the API does not expose a /gametypes
        # endpoint for creating game types
        gametype = Game_Type()
        gametype.label = "Board game"
        gametype.save()


        game = Game()
        game.game_type_id = 1
        game.title = "Sorry"
        game.gamer_id = 1
        game.number_of_players = 4
        game.description = "fun"
        game.save()
        

    def test_create_event(self):
        """
        Ensure we can create a new game.
        """
        # DEFINE GAME PROPERTIES
        url = "/events"
        data = {
            "event_time": "2020-08-28T14:51:39.989Z",
            "gameId": 1,
            "gamerId": 1,
            "location": "Shelbyville"
        }


        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["event_time"], "2020-08-28T14:51:39.989Z")
        # self.assertEqual(json_response["game"]["id"], 2)
        # self.assertEqual(json_response["gamer"]["id"], 2)
        # self.assertEqual(json_response["game_type"]["id"], 1)
        self.assertEqual(json_response["location"], "Shelbyville")

      

    def test_get_event(self):
        """
        Ensure we can get an existing game.
        """

        # Seed the database with a game
        event = Event()
        event.event_time = "2020-08-28T14:51:39.989Z"
        event.location = "Shelbyville"
        event.game_id = 1
        event.gamer_id = 1
        event.save()
        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.get(f"/events/{event.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        # self.assertEqual(json_response["event_time"], "2020-08-28T14:51:39.989Z")
        self.assertEqual(json_response["game"]["id"], 1)
        self.assertEqual(json_response["gamer"]["id"], 1)
        self.assertEqual(json_response["location"], "Shelbyville")

    def test_change_event(self):
        """
        Ensure we can get an existing game.
        """

        # Seed the database with a game
        event = Event()
        event.event_time = "2020-08-28T14:51:39.989Z"
        event.location = "Shelbyville"
        event.game_id = 1
        event.gamer_id = 1
        event.save()

        data = {
            "event_time": "2020-08-28T14:51:39.989Z",
            "gameId": 1,
            "gamerId": 1,
            "location": "Shelbyville"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(f"/events/{event.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET GAME AGAIN TO VERIFY CHANGES
        response = self.client.get(f"/events/{event.id}")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the properties are correct
        self.assertEqual(json_response["event_time"], "2020-08-28T14:51:39.989Z")
        self.assertEqual(json_response["game"]["id"], 1)
        self.assertEqual(json_response["gamer"]["id"], 1)
        self.assertEqual(json_response["location"], "Shelbyville")


    def test_delete_event(self):
        """
        Ensure we can delete an existing game.
        """
        event = Event()
        event.event_time = "2020-08-28T14:51:39.989Z"
        event.location = "Shelbyville"
        event.game_id = 1
        event.gamer_id = 1
        event.save()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(f"/events/{event.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET event AGAIN TO VERIFY 404 response
        response = self.client.get(f"/events/{event.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        
