#!/bin/env bash

# Make sure only root can run our script
if [[ $EUID -ne 0 ]]; then
   echo "$0 must be run as root" 1>&2
   exit 1
fi

fio_location=$(which fio 2>1)
if [ -z ${fio_location} ]
then
	echo "fio is not installed."
	echo -e "Please install fio using:\n\n    yum install fio -y\n"
	exit 1
fi

now=$(date +"%Y%m%d_%H%M%S")
ClusterMembership=$(grep ClusterMembership /etc/cb/cb.conf | awk -F'=' '{print $2}')
cb_data_dir=$(grep DatastoreRootDir /etc/cb/cb.conf  | awk -F'=' '{print $2 "/"}')
fio_config_dir=$(grep "directory=" /usr/share/cb/diag/basic_rw_randseq_tests.fio | awk -F '=' '{print $2}')

if [ ${cb_data_dir} != ${fio_config_dir} ]
then
	echo "Modified fio config file /usr/share/cb/diag/basic_rw_randseq_tests.fio to match the CB Data Directory."
	for fl in /usr/share/cb/diag/basic_rw_randseq_tests.fio
	do
    	mv $fl $fl.${now}
     	sed "s|directory=.*$|directory=${cb_data_dir}|g" $fl.${now} > $fl
	done
fi

disk_free=$(df -k ${cb_data_dir} | grep -v Used | awk -F' '  'NR >1 {print $3}')
disk_free=$((${disk_free} * 1024 ))

min_free=16000000000
if [ ${disk_free} -le ${min_free} ]
	then
	echo "${cb_data_dir} freespace = ${disk_free} bytes"
	echo "Test requires minimum of 16 GB free space in ${cb_data_dir}"
	echo "Insufficient freespace, exiting without testing FIO."
	exit 1
fi

service_status=$(service cb-enterprise status | grep -v stopped )

if [ -n "${service_status}" ]
then
	echo "${service_status}"
	echo "cb-enterprise service(s) still running."
	echo "fio test must be run with CB services halted."
	if [ ${ClusterMembership} == 'Standalone' ]
	then
		read -p "Shall we stop them for you? [y/N]: " yn
    	case $yn in
        	[Yy]* ) service cb-enterprise stop ;;
        	* ) echo "Exiting script so you can stop the services." ; exit 1;;
    	esac
	else
		echo "this server is part of a clustered environment."
		echo "exiting the script so you can stop the cluster."
		exit 1
	fi
fi

token=$(cat /etc/cb/server.token | grep "token=" | awk -F '=' '{print $2}')
results="fio_results_${token}_${now}.txt"

echo "Changing directory to ${cb_data_dir}"
cd ${cb_data_dir}

echo "Running FIO test now."
echo "Results will be written to ${cb_data_dir}${results}"
echo -e "The test may take up to 4 minutes to complete.\n"

#fio /usr/share/cb/diag/basic_rw_randseq_tests.fio --output ${cb_data_dir}${results}
echo "token=${token}" >> ${cb_data_dir}${results}

rm ${cb_data_dir}random-reads.1.0 2> /dev/null
rm ${cb_data_dir}sequential-reads.2.0 2> /dev/null
rm ${cb_data_dir}random-writes.3.0 2> /dev/null
rm ${cb_data_dir}sequential-writes.4.0 2> /dev/null

for filename in $(ls ${cb_data_dir}{random,sequential}-* 2>/dev/null)
do
    echo "${filename} remains on disk.  Please manually remove it."
done

if [ ${ClusterMembership} == 'Standalone' ]
then
	read -p "Shall we start the CB services for you? [y/N]: " yn
	case $yn in
		[Yy]* ) service cb-enterprise start ;
			read -p "Shall we upload the results to Carbon Black? [y/N]: " upyn
			case $upyn in
				[Yy]* ) /usr/share/cb/cbpost ${cb_data_dir}${results} ;;
				* ) echo -e "To send results to CB support issue the following command:\n\n/usr/share/cb/cbpost ${cb_data_dir}${results}\n\n" ;;
			esac ;;
		* ) echo "Tests completed.  Please restart cb-enterprise" ;;
	esac
else
	echo "This server is part of a clustered environment."
	echo "Please start the cluster once testing is complete."
	echo -e "To send results to CB support, after starting cb-enterprise, issue the following command:\n\n/usr/share/cb/cbpost ${cb_data_dir}${results}\n\n"
	
fi




