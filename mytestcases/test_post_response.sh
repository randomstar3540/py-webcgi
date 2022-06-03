cd ..
python3 webserv.py config.cfg &
PID=$!
cd -
sleep 0.2
curl --data "param1=1&param2=2" 127.0.0.1:8070/ 2> /dev/null |diff - out/post_response.out
kill $PID
