cd ..
python3 webserv.py config.cfg &
PID=$!
cd -
sleep 0.2
curl -I 127.0.0.1:8070/mystyle.css 2> /dev/null |diff - out/style.out
kill $PID
