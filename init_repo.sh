#!/bin/bash
git init
git add .
git commit -m "Initial production code release for castdisp framework platforms"
git branch -M main
git remote add origin https://github.com/dharmendra30/castdisp.git
echo "Workspace setup successfully. Run 'git push -u origin main --tags' after setting release labels!" 