NAME=a_maze_ing.py
FLAKE=flake8
MYPY=mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
MYPY_STRICT= mypy . --warn-return-any
VENV=venv
CONFIG= config/config.txt
venv:
	uv  venv $(VENV)

run:
	@python3 $(NAME) $(CONFIG)

lt: 
	@$(MYPY)

lt_strict: 
	@$(MYPY_STRICT)

lint:
	@make -i -s lt
	flake8 .

lint-strict:
	@make -i -s lt_strict
	flake8 .

clean:
	find . -type d \( -name "*.mypy_cache" -o -name "*__pycache__" -name ".venv" \) -exec rm -rf {} \;

fclean: clean
	rm -rf $(VENV)

COM= generic_com
git:
	@make -i -s clean
	git add .
	git commit -m  $(COM)
	git push origin $(shell git branch --show-current)

.PHONY: venv run lt lint clean fclean git 