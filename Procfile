user: hypercorn user --reload --debug --bind user.local.gd:5000 --access-logfile - --error-logfile - --log-level DEBUG

# game1: hypercorn game --reload --debug --bind game.local.gd:5100 --access-logfile - --error-logfile - --log-level DEBUG
# game2: hypercorn game --reload --debug --bind game.local.gd:5200 --access-logfile - --error-logfile - --log-level DEBUG
# game3: hypercorn game --reload --debug --bind game.local.gd:5300 --access-logfile - --error-logfile - --log-level DEBUG

primary:./bin/litefs -config ./etc/primary.yml
secondary1:./bin/litefs -config ./etc/secondary1.yml
secondary2:./bin/litefs -config ./etc/secondary2.yml

leaderboard: hypercorn redis_client --reload --debug --bind leaderboard.local.gd:5400 --access-logfile - --error-logfile - --log-level DEBUG
