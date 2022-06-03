cd ..
python3 webserv.py config.cfg &
PID=$!
cd -
sleep 0.2
curl 127.0.0.1:8070/post.html 2> /dev/null |diff - out/post_html.out
kill $PID
