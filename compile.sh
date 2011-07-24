#!/bin/sh

cd $(dirname $0)

for i in `ls po/*.po`;do
	echo "Compiling `echo $i|sed "s|po/||"`"
	msgfmt $i -o `echo $i |sed "s/.po//"`.mo
done
intltool-merge po/ -d -u src/setupcenter.desktop.in src/setupcenter.desktop
intltool-merge po/ -d -u src/setupcenter-kde.desktop.in src/setupcenter-kde.desktop
