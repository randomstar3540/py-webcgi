cd ..
python3 webserv.py config.cfg &
PID=$!
cd -
sleep 0.2
curl 127.0.0.1:8070/cgibin/reallyslow.py 2> /dev/null |diff - out/mutiple3_1.out || curl 127.0.0.1:8070/greetings.html 2> /dev/null |diff - out/mutiple3_2.out
kill $PID
