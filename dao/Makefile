install:
	sudo apt install jq
	pip install -r requirements.txt

wamp_dao_contributors:
	python wamp_dao_contrib.py --output wamp-dao-contrib.json
	jq . wamp-dao-contrib.json > wamp-dao-contrib-pp.json

contributors:
	jq . wamp-dao-contrib.json
