cd ..
python3 webserv.py config.cfg &
PID=$!
cd -
sleep 0.2
curl 127.0.0.1:8070/myxml.xml 2> /dev/null |diff - out/xml_content.out
kill $PID
