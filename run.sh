#! /bin/bash
mod_wsgi-express start-server sysinfo.wsgi --server-root httdump/ &
curl localhost:8000