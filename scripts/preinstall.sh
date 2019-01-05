#!/bin/bash
echo running command "[id -u myuser]"
id -u myuser 
if [ $? -eq 0 ]; then
echo "user myuser exists, skipping.."
else
echo "myuser does not exist.."
echo "creating myuser.."
useradd myuser
fi 

echo running command "[getent group mygroup]"
getent group mygroup 
if [ $? -eq 0 ]; then
echo "group mygroup exists, skipping.."
else
echo "mygroup does not exist.."
echo "creating mygroup.."
groupadd mygroup
fi

