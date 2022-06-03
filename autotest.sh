set -e
cd mytestcases
for file in *.sh;
do
  echo testing "$file"
  bash "$file" -H
done