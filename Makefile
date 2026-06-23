NAME=a_maze_ing.py
FLAKE=flake8
MYPY=mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
VENV=venv
CONFIG= config/config.txt
venv:
	uv  venv $(VENV)

run:
	@python3 $(NAME) $(CONFIG)

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
	@make -i -s clean
	git add .
	git commit -m  $(COM)
	git push origin $(shell git branch --show-current)

.PHONY: venv run lt lint clean fclean git 