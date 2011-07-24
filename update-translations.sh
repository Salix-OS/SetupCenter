#!/bin/sh

intltool-extract --type="gettext/ini" src/setupcenter.desktop.in
intltool-extract --type="gettext/ini" src/setupcenter-kde.desktop.in

xgettext --from-code=utf-8 \
	-L Glade \
	-o po/setupcenter.pot \
	src/setupcenter.glade

xgettext --from-code=utf-8 \
	-j \
	-L Python \
	-o po/setupcenter.pot \
	src/setupcenter.py

xgettext --from-code=utf-8 \
        -j \
        -L C -kN_ \
        -o po/setupcenter.pot \
        src/setupcenter.desktop.in.h

xgettext --from-code=utf-8 \
        -j \
        -L C -kN_ \
        -o po/setupcenter.pot \
        src/setupcenter-kde.desktop.in.h

xgettext --from-code=utf-8 \
        -j \
	-L Python \
        -o po/setupcenter.pot \
        src/setupcenter_pref.py

rm src/setupcenter.desktop.in.h src/setupcenter-kde.desktop.in.h

cd po
for i in `ls *.po`; do
	msgmerge -U $i setupcenter.pot
done
rm -f ./*~
