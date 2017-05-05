@echo off
cls

echo **************************** > foo2.txt
echo *         DATE             *  >> foo2.txt
echo ****************************  >> foo2.txt
echo %DATE% >> foo2.txt
echo.  >> foo2.txt
echo ****************************  >> foo2.txt
echo *         TIME             *  >> foo2.txt
echo ****************************  >> foo2.txt
echo %TIME% >> foo2.txt
echo.  >> foo2.txt
echo ****************************  >> foo2.txt
echo *         SYSTEMINFO       *  >> foo2.txt
echo ****************************  >> foo2.txt
systeminfo  >> foo2.txt
echo ****************************  >> foo2.txt
echo *         NET USER         *  >> foo2.txt
echo ****************************  >> foo2.txt
net user  >> foo2.txt
echo.  >> foo2.txt
echo ****************************  >> foo2.txt
echo *         NET GROUP        *  >> foo2.txt
echo ****************************  >> foo2.txt
::net group  >> foo2.txt
echo.  >> foo2.txt
echo ****************************  >> foo2.txt
echo *         IP CONFIG        *  >> foo2.txt
echo ****************************  >> foo2.txt
ipconfig /all  >> foo2.txt
echo.  >> foo2.txt
echo ****************************  >> foo2.txt
echo *         ROUTE TABLE      *  >> foo2.txt
echo ****************************  >> foo2.txt
route print  >> foo2.txt
echo.  >> foo2.txt
echo ****************************  >> foo2.txt
echo *         ARP TABLE        *  >> foo2.txt
echo ****************************  >> foo2.txt
arp -a  >> foo2.txt
echo.  >> foo2.txt
echo ****************************  >> foo2.txt
echo *         DNS INFO         *  >> foo2.txt
echo ****************************  >> foo2.txt
ipconfig /displaydns  >> foo2.txt
echo.  >> foo2.txt
echo ****************************  >> foo2.txt
echo *         NETSTAT          *  >> foo2.txt
echo ****************************  >> foo2.txt
netstat -abn  >> foo2.txt
echo.  >> foo2.txt
