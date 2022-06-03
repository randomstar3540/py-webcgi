cd ..
python3 webserv.py config.cfg &
PID=$!
cd -
sleep 0.2
curl --data "param1=1&param2=2" http://127.0.0.1:8070/cgibin/contentlength.py 2> /dev/null |diff - out/cgi_environ1.out
kill $PID
