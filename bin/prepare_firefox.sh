
firefox > /dev/null 2>&1 &
sleep 5
killall firefox || true
killall crashreporter || true

