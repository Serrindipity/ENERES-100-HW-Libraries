build_venv = p"~/.virtualenvs/.venv-build/bin/python3"
library_venv = p"~/.virtualenvs/.math-venv/bin/python3"

# Testing first
cd "~/Projects/ENERES-100-HW-Libraries"
test = !(@(library_venv) -m eneres_100_hw_libraries.tests.test_reprs)
if test.returncode:
    print(test.errors)
    print("Test Failed. Aborting build.")
    exit

cd "~/Projects/eneres_100_unum"
if "nothing to commit, working tree clean" not in !(git status).out:
    @(build_venv) -m build
    git add .
    msg = input("Please enter a commit message for eneres_100_unum: \n")
    git commit -m @(msg)
git push

cd "~/Projects/ENERES-100-HW-Libraries"
if "nothing to commit, working tree clean" not in !(git status).out:
    @(build_venv) -m build
    git add .
    msg = input("Please enter a commit message for ENERES-100-HW-Libraries: \n")
    git commit -m @(msg)
git push

@(library_venv) -m pip uninstall -y eneres_100_unum eneres_100_hw_libraries
@(library_venv) -m pip install "eneres_100_hw_libraries@git+https://github.com/Serrindipity/ENERES-100-HW-Libraries.git@main"

