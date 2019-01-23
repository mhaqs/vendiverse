echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device

hwclock -s -f /dev/rtc1

date +%Y%m%d -s "20170330"

date +%T -s "14:32:57"

hwclock -w
