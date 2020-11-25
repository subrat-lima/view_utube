all: utube

utube:
	chmod +x utube_scraper.py utube.py
	mkdir -p ${HOME}/.local/utube/
	cp utube_scraper.py ${HOME}/.local/bin/utube_scraper.py
	cp utube.py ${HOME}/.local/bin/utube
	crontab ./scripts/scrape.cron

scripts:
	cp ./scripts/downloadYT ${HOME}/.local/bin/
	cp ./scripts/watchYT ${HOME}/.local/bin/
	cp ./scripts/ytube ${HOME}/.local/bin/

demo:
	touch ${HOME}/.local/utube/data.txt
	touch ${HOME}/.local/utube/channels.txt
