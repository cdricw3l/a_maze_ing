NAME=a_maze_ing.py
FLAKE=flake8
PDB=-m pdb 
MYPY=mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
MYPY_STRICT=mypy . --strict
VENV=venv
CONFIG= config/config.txt
OUTPUT = output_maze.txt

venv:
	uv  venv $(VENV)

install:
	@echo "No package to install."

run:
	@python3 $(NAME) $(CONFIG)

debug:
	@python3 $(PDB) $(NAME) $(CONFIG)

clean:
	@find . -type d \( -name "*.mypy_cache" -o -name "*__pycache__" -o  -name "*venv" \) 2> /dev/null -exec rm -rf {} \;

lt: 
	$(MYPY)

lt_strict: 
	$(MYPY_STRICT)

lint:
	make -i -s lt
	flake8 .

lint-strict:
	make -i -s lt_strict
	flake8 .

COM= generic_com
git:
	@make -i -s clean
	git add .
	git commit -m  $(COM)
	git push origin $(shell git branch --show-current)

.PHONY: venv run lt lint lint clean fclean git 