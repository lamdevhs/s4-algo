
for f in Dico.py A.py C.py Tests_A.py Tests_B.py Tests_C.py B.py ; do
  echo ___________________
  echo ////////// $f
  python3 "$f"
done