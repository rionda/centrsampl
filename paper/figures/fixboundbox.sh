#! /bin/sh
if [ $# -lt 1 ]; then
  echo "usage: $0 outputdir" > /dev/stderr
fi

for FILE in `ls *.eps`; do
  epstool --copy --bbox $FILE $1/$FILE
done

