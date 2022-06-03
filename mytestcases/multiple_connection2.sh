cd ..
python3 webserv.py config.cfg &
PID=$!
cd -
sleep 0.2
curl 127.0.0.1:8070/cgibin/hello.py 2> /dev/null |diff - out/mutiple2_1.out || curl 127.0.0.1:8070/home.js 2> /dev/null |diff - out/mutiple2_2.out
kill $PID
