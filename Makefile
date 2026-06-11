NAME= a_maze_ing.py
FLAKE= flake8
MYPY=mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

venv:
	python3 -m venv venv

run:
	python3 $(NAME)

lt: 
	@$(FLAKE)
	@$(MYPY)

lint:
	@make -i lt

clean:
	find .  \( -name __pycache__ -o -name .mypy_cache\)

COM= generic_com
git:
	git add .
	git commit -m  $(COM)
	git push origin $(shell git branch --show-current)