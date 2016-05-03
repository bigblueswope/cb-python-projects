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
	echo "cb-enterprise service(s) still running. Please stop the services before running the test."
	exit 1
fi

token=$(cat /etc/cb/server.token | grep "token=" | awk -F '=' '{print $2}')
results="fio_results_${token}_${now}.txt"

echo "Changing directory to ${cb_data_dir}"
cd ${cb_data_dir}

echo "Running FIO test now."
echo "Results will be written to ${results}"
echo -e "The test may take up to 4 minutes to complete.\n"

fio /usr/share/cb/diag/basic_rw_randseq_tests.fio --output ${results}
echo "token=${token}" >> ${results}

for filename in $(ls ${cb_data_dir}{random,sequential}-* 2>/dev/null)
do
    echo "${filename} remains on disk.  Please manually remove it."
done

echo -e "To send results to CB support, after starting cb-enterprise, issue the following command:\n\n/usr/share/cb/cbpost ${results}\n\n"

echo "Tests completed.  Please restart cb-enterprise"


