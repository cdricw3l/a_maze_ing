NAME=a_maze_ing.py
FLAKE=flake8
PDB=-m pdb 
MYPY=mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
MYPY_STRICT=mypy . --strict
CONFIG= config.txt
OUTPUT = output_maze.txt


venv:
	@uv venv $(VENV)

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
	@$(MYPY)

lt_strict: 
	@$(MYPY_STRICT)

lint:
	@make -i -s lt
	flake8 .

lint-strict:
	@make -i -s lt_strict
	flake8 .

.PHONY: venv run lt lt_strict lint lint-strict clean find_and_remove debug install