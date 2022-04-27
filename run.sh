#! /bin/bash
~/.local/bin/mod_wsgi-express start-server sysinfo.wsgi --server-root httdump/ &
sleep(10)
curl localhost:8000