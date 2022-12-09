import collections
import dataclasses
import databases
import textwrap
import redis

from pydoc import doc
from quart import Quart, g, request, abort
from quart_schema import QuartSchema, RequestSchemaValidationError, validate_request

app = Quart(__name__)
QuartSchema(app)

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, charset='utf-8', decode_responses=True)

@dataclasses.dataclass
class LeaderboardInformation:
    username: str
    num_guesses: int
    game_result: str

@app.route("/results", methods=["POST"])
@validate_request(LeaderboardInformation)
async def user_data(data):
    results = dataclasses.asdict(data)
    username = results['username']
    num_guesses = results['num_guesses']
    win_loss = results['game_result']
    score, average_score, num_games = 0, 0, 1

    if win_loss == 'win':
        get_score = {1: 6, 2: 5, 3: 4, 4: 3, 5: 2, 6: 1}
        score = get_score[num_guesses]

    game_data = str(f'{score}:{num_games}')
    if redis_client.hget('Scores', username) == None:
        redis_client.hset('Scores', username, game_data)
        redis_client.hset('Averages', username, score)
    else:
        game_data = redis_client.hget('Scores', username)
        score = int(game_data.split(':')[0])
        num_games = int(game_data.split(':')[1])
        score += get_score[num_guesses]
        num_games += 1
        average_score = int(score/num_games)
        game_data = str(f'{score}:{num_games}')
        redis_client.hset('Scores', username, game_data)
        redis_client.hset('Averages', username, average_score)

    return LeaderboardInformation, 201

@app.route("/leaderboard", methods=["GET"])
async def create_board():
    pass

# import redis
# r = redis.Redis()
# # hset(name, key=None, value=None, mapping=None, items=None)
# userid = 10
# score = [6, 7, 8]
# gameid = [5, 6, 7]
# total_score = num_of_scores = 0
# for i in range(len(gameid)):
#     r.hset("Scores", gameid[i], score[i])
# for i in range(len(gameid)):
#     total_score += int(r.hget("Scores", userid))
#     num_of_scores += 1
# print(total_score/num_of_scores)
# # To get someone's score, average all of the scores from their games
# # So we store the scores using userid as the key  and the score as the value
# # userid = 1
# # scores = [5, 7, 9]
# # r.mset({userid: 5})
# # r.mset({userid: 7})
# # r.mset({userid: 9})
# # print(r.hkeys(userid))
