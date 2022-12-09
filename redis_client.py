import collections
import dataclasses
import databases
import redis

from quart import Quart, request, abort, g
from quart_schema import QuartSchema, RequestSchemaValidationError, validate_request


app = Quart(__name__)
QuartSchema(app)


redis_client = redis.Redis(host='localhost', port=6379, db=0, charset='utf-8', decode_responses=True)


@dataclasses.dataclass

class LeaderboardInformation:
    username: str
    result: str
    guesses: int


@app.route("/results", methods=["POST"])

@validate_request(LeaderboardInformation)

async def user_data(data):
    results = dataclasses.asdict(data)
    username = results['username']
    num_guesses = results['guesses']
    win_loss = results['result']
    
    score, average_score, num_games = 0, 0, 1

    if num_guesses > 6 or num_guesses < 1:

        return {'Error':"Incorrect guesses! (out of bounds)"}

    else:
        if win_loss == 'win':
            get_score = {1: 6, 2: 5, 3: 4, 4: 3, 5: 2, 6: 1}
            score = get_score[num_guesses]
        elif win_loss == 'loss':
            score = 0
        else:
            return {'Error' : 'Incorrect result string'}, 404
        
        if redis_client.hget('Scores', 'username') == username:
            score = int(redis_client.hget("Scores", 'score')) + score
            num_games = int(redis_client.hget("Scores", 'game_count')) + num_games
            average_score = int(score/num_games)
            
            redis_client.hset('Scores', 'username', username)
            redis_client.hset('Scores', 'game_count', num_games)
            redis_client.hset('Scores', 'result', win_loss)
            redis_client.hset('Scores', 'score', score)
            redis_client.hset('Scores', 'average_score', average_score)
            
            value = redis_client.zadd("LeaderBoard", {username : average_score})
            
        else:
            redis_client.hset('Scores', 'username', username)
            redis_client.hset('Scores', 'game_count', num_games)
            redis_client.hset('Scores', 'result', win_loss)
            redis_client.hset('Scores', 'score', score)
            redis_client.hset('Scores', 'average_score', score)
            
            value = redis_client.zadd("LeaderBoard" , {username : score})
            
        return redis_client.hgetall('Scores'), 200
        
@app.route("/LeaderBoard/", methods=["GET"])

async def scores():
    
    scorestop = redis_client.zrange("LeaderBoard", 0, 9, desc = True, withscores = True)
    
    if scorestop != []:    
        return ('\n'.join(map(str, scorestop))), 200
       
    
    else:
        return {"Error": "No data"}, 404 
        
    
