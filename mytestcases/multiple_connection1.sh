cd ..
python3 webserv.py config.cfg &
PID=$!
cd -
sleep 0.2
curl 127.0.0.1:8070/index.html 2> /dev/null |diff - out/mutiple1_1.out || curl 127.0.0.1:8070/greetings.html 2> /dev/null |diff - out/mutiple1_2.out
kill $PID
