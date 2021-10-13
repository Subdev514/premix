while true; do
curl 'http://glap-io.pandapip2.repl.co/__tail' > /dev/null &
sleep 10
clear
killall curl
done