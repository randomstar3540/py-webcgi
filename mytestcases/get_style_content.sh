cd ..
python3 webserv.py config.cfg &
PID=$!
cd -
sleep 0.2
curl 127.0.0.1:8070/mystyle.css 2> /dev/null |diff - out/style_content.out
kill $PID
