set -e

vuepress build docs

cd docs/.vuepress/dist

git init
git add -A
git commit -m 'deploy'

cd -