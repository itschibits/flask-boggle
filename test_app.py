from unittest import TestCase

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            html = response.get_data(as_text=True)
            # test that you're getting a template
            self.assertIn('<button class="word-input-btn">Go</button>', html)
            self.assertIn("Boggle homepage. used in test, don't remove", html)

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            response = client.get('/api/new-game')
            json_dict = response.get_json()
            board = json_dict['board']

            print(response)
            # write a test for this route

            self.assertIn('gameId', json_dict)
            self.assertTrue(isinstance(board, list), True)

    def test_score_word(self):
        """Test scoring a played word"""
        with self.client as client:
            response = client.get('/api/new-game')
            json_dict = response.get_json()
            game_id = json_dict['gameId']
            game = games[game_id]
            game.board[0] = ["E", "U", "S", "S", "O"]
            game.board[1] = ["A", "E", "R", "R", "U"]
            game.board[2] = ["N", "A", "O", "E", "T"]
            game.board[3] = ["I", "E", "C", "Y", "M"]
            game.board[4] = ["T", "R", "E", "E", "Z"]

            response = client.post(
                    '/api/score-word',
                    json={"word": "tree", "gameId": game_id}
                    )

            self.assertEqual(response.get_json(), {"result": "ok"})

            response = client.post(
                    '/api/score-word',
                    json={"word": "sort", "gameId": game_id}
                    )

            self.assertEqual(response.get_json(), {"result": "ok"})

            response = client.post(
                    '/api/score-word',
                    json={"word": "zonally", "gameId": game_id}
                    )

            self.assertEqual(response.get_json(), {"result": "not-on-board"})

            response = client.post(
                    '/api/score-word',
                    json={"word": "EUSSOURREAN", "gameId": game_id}
                    )

            self.assertEqual(response.get_json(), {"result": "not-word"})
