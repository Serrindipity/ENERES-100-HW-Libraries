cd "~/Projects/eneres_100_unum"

"~/.virtualenvs/.venv-build/bin/python3" -m build

git add .
msg = input("Please enter a commit message for eneres_100_unum: \n")
git commit -m @(msg)
git push
sleep .5

cd "~/Projects/ENERES-100-HW-Libraries"
"~/.virtualenvs/.venv-build/bin/python3" -m build
git add .
msg = input("Please enter a commit message for ENERES-100-HW-Libraries: \n")
git commit -m @(msg)
git push
sleep .5

"~/.virtualenvs/.math-venv/bin/python3" -m pip uninstall -y eneres_100_unum eneres_100_hw_libraries
sleep 1
"~/.virtualenvs/.math-venv/bin/python3" -m pip install "eneres_100_hw_libraries@git+https://github.com/Serrindipity/ENERES-100-HW-Libraries.git@main"

