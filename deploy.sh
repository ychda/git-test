#git remote add origin git@github.com:ychda/git-test.git
git add --all
git commit -m "从main分支增加一个文件"
git push -u origin master

git status
git branch -a
git log --graph
git checkout -b main
