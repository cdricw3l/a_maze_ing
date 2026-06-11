NAME= a_maze_ing.py

venv:
	python3 -m venv venv

run:
	python3 $(NAME)

COM= generic_com
git:
	git add .
	git commit -m  $(COM)
	git push origin $(shell git branch --show-current)