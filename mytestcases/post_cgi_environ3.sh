cd ..
python3 webserv.py config.cfg &
PID=$!
cd -
sleep 0.2
curl --data "thisisasuperlongparam=supersuperlong&thisisasuperlongparam2=supersuperlong2" http://127.0.0.1:8070/cgibin/contentlength.py 2> /dev/null |diff - out/cgi_environ3.out
kill $PID
