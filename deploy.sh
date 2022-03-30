#git remote add origin git@github.com:ychda/git-test.git
git add --all
git commit -m "合并分支后修改了deploy.sh文件"
#git push -u origin main
git push -u origin master

git status
git branch -a
git log --graph
git checkout -b main


#
# git checkout master
# git merge --no-ff main
# git branch -d main
#
