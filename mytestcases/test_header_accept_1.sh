cd ..
python3 webserv.py config.cfg &
PID=$!
cd -
sleep 0.2
curl -I "Accept: text/html" 127.0.0.1:8070 2> /dev/null | diff - out/accept_1.out
kill $PID