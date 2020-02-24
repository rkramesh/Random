#!/system/bin/sh
#/system/bin/insmod /data/local/tmp/rockchip-cir.ko
cd /data/local/tmp
./ir-keytable -p NEC
./ir-keytable -c
#./ir-keytable -w samsung.map
./ir-keytable -w new.map
