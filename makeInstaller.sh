pyinstaller manage.py

rm -rf /tmp/productManager/
mkdir -p /tmp/productManager/DEBIAN
mkdir -p /tmp/productManager/opt/productManager/

cp -r ./dist/manage/ /tmp/productManager/opt/productManager/

echo -e "Package: productManager" > /tmp/productManager/DEBIAN/control
echo -e "Version: 1.0" >> /tmp/productManager/DEBIAN/control
echo -e "Architecture: amd64" >> /tmp/productManager/DEBIAN/control
echo -e "Maintainer: Daniel Badinszky <badinszky97@gmail.com>" >> /tmp/productManager/DEBIAN/control
echo -e "Description: An application for managing a BOM hierarchy of a small/medium company." >> /tmp/productManager/DEBIAN/control


chmod +x /tmp/productManager/opt/productManager/manage/manage


cat <<EOF >> /tmp/productManager/DEBIAN/postinst
#!/bin/bash

# media mappa letrehozasa:
mkdir -p /var/product_manager/

EOF

chmod 775 /tmp/productManager/DEBIAN/postinst

cd /tmp
dpkg-deb --build productManager