NAME=a_maze_ing.py
FLAKE=flake8
MYPY=mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
VENV=venv

venv:
	python3 -m venv $(venv)

run:
	python3 $(NAME)

lt: 
	@$(MYPY)

lint:
	@make -i -s lt

clean:
	find . -type d \( -name "*.mypy_cache" -o -name "*__pycache__" \) -exec rm -rf {} \;

fclean: clean
	rm -rf $(VENV)

COM= generic_com
git:
	git add .
	git commit -m  $(COM)
	git push origin $(shell git branch --show-current)

.PHONY: venv run lt lint clean fclean git 