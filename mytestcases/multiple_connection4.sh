cd ..
python3 webserv.py config.cfg &
PID=$!
cd -
sleep 0.2
start=$SECONDS
curl 127.0.0.1:8070/cgibin/reallyslow.py 2> /dev/null |diff - out/mutiple4_1.out || curl 127.0.0.1:8070/cgibin/also_reallyslow.py 2> /dev/null |diff - out/mutiple4_2.out
duration=$(( SECONDS - start ))
echo Two slow file, one takes 5 sec and one takes 4 sec, 9 sec total, but only takes $duration sec here!
kill $PID
