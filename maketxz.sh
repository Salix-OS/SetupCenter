#!/bin/sh

cd $(dirname $0)
./compile.sh
mkdir -p pkg
export DESTDIR=$PWD/pkg
./install.sh
VER=$(grep 'version =' src/setupcenter.py | head -n 1 | sed "s/.*'\(.*\)'/\1/" | tr -d '-')
cd pkg
cat <<EOF > install/slack-desc
setupcenter: SetupCenter - A centralized setup panel.
setupcenter:
setupcenter: SetupCenter offers a centralized spot for all your system
setupcenter: utilities. Its default settings are highly configurable.
setupcenter: The view layout, the categories, the icons used, the 
setupcenter: selection of utilities and even its displayed name are all 
setupcenter: fully customizable.
setupcenter:
setupcenter:
setupcenter:
setupcenter:
EOF
makepkg -l y -c n ../setupcenter-$VER-noarch-1plb.txz
cd ..
echo -e "python,pygtk,pyxdg" > setupcenter-$VER-noarch-1plb.dep
md5sum setupcenter-$VER-noarch-1plb.txz > setupcenter-$VER-noarch-1plb.md5
rm -rf pkg
