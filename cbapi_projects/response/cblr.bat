@echo off
cls

echo **************************** > cblr.txt
echo *         DATE             * >> cblr.txt
echo **************************** >> cblr.txt
echo. | date >> cblr.txt
echo. >> cblr.txt
echo **************************** >> cblr.txt
echo *         TIME             * >> cblr.txt
echo **************************** >> cblr.txt
echo. | time >> cblr.txt
echo. >> cblr.txt
echo **************************** >> cblr.txt
echo *         SYSTEMINFO       * >> cblr.txt
echo **************************** >> cblr.txt
echo. | systeminfo >> cblr.txt
echo. >> cblr.txt
echo **************************** >> cblr.txt
echo *         NET USER         * >> cblr.txt
echo **************************** >> cblr.txt
echo. | net user >> cblr.txt
echo. >> cblr.txt
echo **************************** >> cblr.txt
echo *         NET GROUP        * >> cblr.txt
echo **************************** >> cblr.txt
echo. | net group >> cblr.txt
echo. >> cblr.txt
echo **************************** >> cblr.txt
echo *         IP CONFIG        * >> cblr.txt
echo **************************** >> cblr.txt
echo. | ipconfig /all >> cblr.txt
echo. >> cblr.txt
echo **************************** >> cblr.txt
echo *         ROUTE TABLE      * >> cblr.txt
echo **************************** >> cblr.txt
echo. | route print >> cblr.txt
echo. >> cblr.txt
echo **************************** >> cblr.txt
echo *         ARP TABLE        * >> cblr.txt
echo **************************** >> cblr.txt
echo. | arp -a >> cblr.txt
echo. >> cblr.txt
echo **************************** >> cblr.txt
echo *         DNS INFO         * >> cblr.txt
echo **************************** >> cblr.txt
echo. | ipconfig /displaydns >> cblr.txt
echo. >> cblr.txt
echo **************************** >> cblr.txt
echo *         NETSTAT          * >> cblr.txt
echo **************************** >> cblr.txt
echo. | netstat -abn >> cblr.txt
echo. >> cblr.txt
