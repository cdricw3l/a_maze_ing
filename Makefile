NAME=a_maze_ing.py
FLAKE=flake8
PDB=-m pdb 
MYPY=mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
MYPY_STRICT=mypy . --strict
CONFIG= config/config.txt
OUTPUT = output_maze.txt
VENV=venv
MAZE_PACKAGE=dist/mazegen-1.0.0-py3-none-any.whl

venv:
	@uv venv $(VENV)
	@echo "\e[1;34mThe virtual environment (venv) must be activated before running the make mazegen rule!!!\e[1;0m"

mazegen:
	uv build
	uv pip install $(MAZE_PACKAGE)	

install:
	@echo "No package to install."

run:
	@python3 $(NAME) $(CONFIG)

debug:
	@python3 $(PDB) $(NAME) $(CONFIG)

find_and_remove:
	find . -type d \( -name "*.mypy_cache" -o -name "*__pycache__" -o  -name "*venv" \) 2> /dev/null -exec rm -rf {} \;

clean:
	make -s -i find_and_remove

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

.PHONY: venv run lt lint lint clean fclean git mazegen activate deactivate