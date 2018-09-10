#!/bin/bash
echo "copying word docs to Desktop"
cp ./*.docx ~/Desktop/
echo "make lab source code dir /opt/intel/workshop/"
echo intel123 | sudo -S rm -rf /opt/intel/workshop/
echo intel123 | sudo -S mkdir -p /opt/intel/workshop/
echo intel123 | sudo chown intel:intel -R /opt/intel/workshop/
echo "copy lab code to /opt/intel/workshop/"
tar -xf ./*.tar -C /opt/intel/workshop/
echo "All done."
read -p "Press any key to quit..."
