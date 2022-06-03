cd ..
python3 webserv.py config.cfg &
PID=$!
cd -
sleep 0.2
curl -I -H "Accept: image/jpeg" 127.0.0.1:8070 2> /dev/null | grep '406' | diff - out/406_status.out
kill $PID
