@echo off
cls

echo **************************** > system_info.txt
echo *         DATE             *  >> system_info.txt
echo ****************************  >> system_info.txt
echo %DATE% >> system_info.txt
echo.  >> system_info.txt
echo ****************************  >> system_info.txt
echo *         TIME             *  >> system_info.txt
echo ****************************  >> system_info.txt
echo %TIME% >> system_info.txt
echo.  >> system_info.txt
echo ****************************  >> system_info.txt
echo *         SYSTEMINFO       *  >> system_info.txt
echo ****************************  >> system_info.txt
systeminfo  >> system_info.txt
echo ****************************  >> system_info.txt
echo *         NET USER         *  >> system_info.txt
echo ****************************  >> system_info.txt
net user  >> system_info.txt
echo.  >> system_info.txt
echo ****************************  >> system_info.txt
echo *         NET GROUP        *  >> system_info.txt
echo ****************************  >> system_info.txt
::net group  >> system_info.txt
echo.  >> system_info.txt
echo ****************************  >> system_info.txt
echo *         IP CONFIG        *  >> system_info.txt
echo ****************************  >> system_info.txt
ipconfig /all  >> system_info.txt
echo.  >> system_info.txt
echo ****************************  >> system_info.txt
echo *         ROUTE TABLE      *  >> system_info.txt
echo ****************************  >> system_info.txt
route print  >> system_info.txt
echo.  >> system_info.txt
echo ****************************  >> system_info.txt
echo *         ARP TABLE        *  >> system_info.txt
echo ****************************  >> system_info.txt
arp -a  >> system_info.txt
echo.  >> system_info.txt
echo ****************************  >> system_info.txt
echo *         DNS INFO         *  >> system_info.txt
echo ****************************  >> system_info.txt
ipconfig /displaydns  >> system_info.txt
echo.  >> system_info.txt
echo ****************************  >> system_info.txt
echo *         NETSTAT          *  >> system_info.txt
echo ****************************  >> system_info.txt
netstat -abn  >> system_info.txt
echo.  >> system_info.txt
