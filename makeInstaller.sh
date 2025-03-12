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

cat <<EOF >> /tmp/productManager/DEBIAN/postinst
#!/bin/bash

# MariaDB telepitese
while true; do
    # Prompt user for input
    read -p "Install MariaDB? Enter Y for Yes or N for No: " user_input

    # Validate the input
    if [[ "$user_input" == "Y" || "$user_input" == "y" ]]; then
        echo "You selected Yes."
        break
    elif [[ "$user_input" == "N" || "$user_input" == "n" ]]; then
        echo "You selected No."
        break
    else
        echo "Invalid input. Please enter Y or N."
    fi
done

# Megfelelő válasz
if [[ "$user_input" == "Y" || "$user_input" == "y" ]]; then
    echo "Telepithető"
    echo "MariaDB ROOT jelszo:"
    read -r rootpass

    sudo apt update && sudo apt upgrade
    sudo apt -y install software-properties-common
    sudo apt-key adv --fetch-keys 'https://mariadb.org/mariadb_release_signing_key.asc'
    sudo add-apt-repository -y 'deb [arch=amd64] http://mariadb.mirror.globo.tech/repo/10.5/ubuntu $(lsb_release -cs) main'
    sudo apt update
    sudo apt install mariadb-server-11-6-2 mariadb-client
    sudo mysql_secure_installation --set-root-pass=$rootpass --remove-anonymous-user --disallow-root --remove-test-db



    


fi




EOF

chmod +x /tmp/productManager/opt/productManager/manage/manage
chmod 775 /tmp/productManager/DEBIAN/postinst

cd /tmp
dpkg-deb --build productManager