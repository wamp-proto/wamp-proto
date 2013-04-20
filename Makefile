all:
	@echo "Targets:"
	@echo ""
	@echo "  clean"
	@echo "  deploy"
	@echo "  cleandeploy"
	@echo ""

clean:
	echo "Cleaning "wamp.ws" website .."
	sudo rm -rf /usr/local/www/wamp
	sudo mkdir /usr/local/www/wamp

deploy:
	echo "Deploying "wamp.ws" website .."
	sudo cp -R website/* /usr/local/www/wamp

cleandeploy: clean deploy
