Apache Bench
------------

.. code:: bash

    # Install testing tools.
    dnf install httpd-tools
    go get -u github.com/rakyll/hey

    # Generate TLS server certificates
    openssl req -x509 -newkey rsa:4096 -nodes -keyout server.key -out server.crt -days 356 -subj "/C=US/O=Snippy/CN=127.0.0.1"

    # Run HTTP server with sqlite backend with commit f9f418256fccaf7f4c1ee3651b21044aba9a8948 (v0.10.0 + 20 commits)
    docker run --env SNIPPY_SERVER_HOST=127.0.0.1:8080 --net=host --name snippy --detach heilaaks/snippy --defaults
    ab -n 10000 -c 1 -k http://127.0.0.1:8080/api/snippy/rest/snippets?limit=20
    This is ApacheBench, Version 2.3 <$Revision: 1826891 $>
    Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
    Licensed to The Apache Software Foundation, http://www.apache.org/

    Benchmarking 127.0.0.1 (be patient)
    Completed 1000 requests
    Completed 2000 requests
    Completed 3000 requests
    Completed 4000 requests
    Completed 5000 requests
    Completed 6000 requests
    Completed 7000 requests
    Completed 8000 requests
    Completed 9000 requests
    Completed 10000 requests
    Finished 10000 requests


    Server Software:        gunicorn/19.9.0
    Server Hostname:        127.0.0.1
    Server Port:            8080

    Document Path:          /api/snippy/rest/snippets?limit=20
    Document Length:        31914 bytes

    Concurrency Level:      1
    Time taken for tests:   45.854 seconds
    Complete requests:      10000
    Failed requests:        0
    Keep-Alive requests:    0
    Total transferred:      320920000 bytes
    HTML transferred:       319140000 bytes
    Requests per second:    218.08 [#/sec] (mean)
    Time per request:       4.585 [ms] (mean)
    Time per request:       4.585 [ms] (mean, across all concurrent requests)
    Transfer rate:          6834.73 [Kbytes/sec] received

    Connection Times (ms)
                  min  mean[+/-sd] median   max
    Connect:        0    0   0.0      0       0
    Processing:     4    5   0.5      4      15
    Waiting:        4    5   0.5      4      15
    Total:          4    5   0.5      4      15
    WARNING: The median and mean for the processing time are not within a normal deviation
            These results are probably not that reliable.
    WARNING: The median and mean for the waiting time are not within a normal deviation
            These results are probably not that reliable.
    WARNING: The median and mean for the total time are not within a normal deviation
            These results are probably not that reliable.

    Percentage of the requests served within a certain time (ms)
      50%      4
      66%      4
      75%      4
      80%      4
      90%      5
      95%      5
      98%      6
      99%      7
     100%     15 (longest request)

    # Run HTTP server with sqlite backend with commit f9f418256fccaf7f4c1ee3651b21044aba9a8948 (v0.10.0 + 20 commits)
    docker run -d --net="host" --name snippy heilaaks/snippy:latest --server-host 127.0.0.1:8080 --defaults
    /root/go/bin/hey -n 10000 -c 1 http://127.0.0.1:8080/api/snippy/rest/snippets?limit=20

    Summary:
      Total:        45.1121 secs
      Slowest:      0.0142 secs
      Fastest:      0.0044 secs
      Average:      0.0045 secs
      Requests/sec: 221.6700

      Total data:   319140000 bytes
      Size/request: 31914 bytes

    Response time histogram:
      0.004 [1]     |
      0.005 [9974]  |
      0.006 [6]     |
      0.007 [6]     |
      0.008 [3]     |
      0.009 [3]     |
      0.010 [4]     |
      0.011 [2]     |
      0.012 [0]     |
      0.013 [0]     |
      0.014 [1]     |


    Latency distribution:
      10% in 0.0045 secs
      25% in 0.0045 secs
      50% in 0.0045 secs
      75% in 0.0045 secs
      90% in 0.0046 secs
      95% in 0.0046 secs
      99% in 0.0048 secs

    Details (average, fastest, slowest):
      DNS+dialup:   0.0001 secs, 0.0044 secs, 0.0142 secs
      DNS-lookup:   0.0000 secs, 0.0000 secs, 0.0000 secs
      req write:    0.0000 secs, 0.0000 secs, 0.0002 secs
      resp wait:    0.0044 secs, 0.0043 secs, 0.0140 secs
      resp read:    0.0000 secs, 0.0000 secs, 0.0004 secs

    Status code distribution:
      [200] 10000 responses

    # Run HTTPS server with sqlite backend with commit f9f418256fccaf7f4c1ee3651b21044aba9a8948 (v0.10.0 + 20 commits)
    python runner --server-host 127.0.0.1:8080 --server-ssl-cert ./server.crt --server-ssl-key ./server.key --defaults
    /root/go/bin/hey -n 10000 -c 1 https://127.0.0.1:8080/api/snippy/rest/snippets?limit=20

    Summary:
      Total:        90.7888 secs
      Slowest:      0.0161 secs
      Fastest:      0.0088 secs
      Average:      0.0091 secs
      Requests/sec: 110.1457

      Total data:   319140000 bytes
      Size/request: 31914 bytes

    Response time histogram:
      0.009 [1]     |
      0.010 [9856]  |
      0.010 [107]   |
      0.011 [9]     |
      0.012 [5]     |
      0.012 [5]     |
      0.013 [3]     |
      0.014 [1]     |
      0.015 [8]     |
      0.015 [1]     |
      0.016 [4]     |


    Latency distribution:
      10% in 0.0090 secs
      25% in 0.0090 secs
      50% in 0.0090 secs
      75% in 0.0091 secs
      90% in 0.0092 secs
      95% in 0.0093 secs
      99% in 0.0097 secs

    Details (average, fastest, slowest):
      DNS+dialup:   0.0052 secs, 0.0088 secs, 0.0161 secs
      DNS-lookup:   0.0000 secs, 0.0000 secs, 0.0000 secs
      req write:    0.0000 secs, 0.0000 secs, 0.0002 secs
      resp wait:    0.0038 secs, 0.0037 secs, 0.0106 secs
      resp read:    0.0001 secs, 0.0001 secs, 0.0005 secs

    Status code distribution:
      [200] 10000 responses


    # Run HTTP server with PostgreSQL backend with commit f9f418256fccaf7f4c1ee3651b21044aba9a8948 (v0.10.0 + 20 commits)
    docker run -d --net="host" --name snippy heilaaks/snippy --server-host 127.0.0.1:8080 --storage-type postgresql --storage-host localhost:5432 --storage-database postgres --storage-user postgres --storage-password postgres --defaults
    ab -n 10000 -c 1 -k http://127.0.0.1:8080/api/snippy/rest/snippets?limit=20
    This is ApacheBench, Version 2.3 <$Revision: 1826891 $>
    Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
    Licensed to The Apache Software Foundation, http://www.apache.org/

    Benchmarking 127.0.0.1 (be patient)
    Completed 1000 requests
    Completed 2000 requests
    Completed 3000 requests
    Completed 4000 requests
    Completed 5000 requests
    Completed 6000 requests
    Completed 7000 requests
    Completed 8000 requests
    Completed 9000 requests
    Completed 10000 requests
    Finished 10000 requests


    Server Software:        gunicorn/19.9.0
    Server Hostname:        127.0.0.1
    Server Port:            8080

    Document Path:          /api/snippy/rest/snippets?limit=20
    Document Length:        31914 bytes

    Concurrency Level:      1
    Time taken for tests:   52.412 seconds
    Complete requests:      10000
    Failed requests:        0
    Keep-Alive requests:    0
    Total transferred:      320920000 bytes
    HTML transferred:       319140000 bytes
    Requests per second:    190.80 [#/sec] (mean)
    Time per request:       5.241 [ms] (mean)
    Time per request:       5.241 [ms] (mean, across all concurrent requests)
    Transfer rate:          5979.51 [Kbytes/sec] received

    Connection Times (ms)
                  min  mean[+/-sd] median   max
    Connect:        0    0   0.0      0       0
    Processing:     5    5   0.4      5      21
    Waiting:        5    5   0.4      5      21
    Total:          5    5   0.4      5      21

    Percentage of the requests served within a certain time (ms)
      50%      5
      66%      5
      75%      5
      80%      5
      90%      5
      95%      5
      98%      6
      99%      7
     100%     21 (longest request)

    # Run HTTP server with PostgreSQL backend with commit f9f418256fccaf7f4c1ee3651b21044aba9a8948 (v0.10.0 + 20 commits)
    docker run -d --net="host" --name snippy heilaaks/snippy --server-host 127.0.0.1:8080 --storage-type postgresql --storage-host localhost:5432 --storage-database postgres --storage-user postgres --storage-password postgres --defaults
    /root/go/bin/hey -n 10000 -c 1 http://127.0.0.1:8080/api/snippy/rest/snippets?limit=20

    Summary:
      Total:        52.7001 secs
      Slowest:      0.0211 secs
      Fastest:      0.0050 secs
      Average:      0.0053 secs
      Requests/sec: 189.7530

      Total data:   319140000 bytes
      Size/request: 31914 bytes

    Response time histogram:
      0.005 [1]     |
      0.007 [9968]  |
      0.008 [9]     |
      0.010 [6]     |
      0.011 [8]     |
      0.013 [0]     |
      0.015 [1]     |
      0.016 [1]     |
      0.018 [1]     |
      0.020 [3]     |
      0.021 [2]     |


    Latency distribution:
      10% in 0.0051 secs
      25% in 0.0052 secs
      50% in 0.0053 secs
      75% in 0.0053 secs
      90% in 0.0054 secs
      95% in 0.0054 secs
      99% in 0.0058 secs

    Details (average, fastest, slowest):
      DNS+dialup:   0.0001 secs, 0.0050 secs, 0.0211 secs
      DNS-lookup:   0.0000 secs, 0.0000 secs, 0.0000 secs
      req write:    0.0000 secs, 0.0000 secs, 0.0002 secs
      resp wait:    0.0051 secs, 0.0048 secs, 0.0209 secs
      resp read:    0.0000 secs, 0.0000 secs, 0.0003 secs

    Status code distribution:
      [200] 10000 responses

    # HTTP server with PyPy and Sqlite as storage backed (comment psycopg2 out from setup)
    sudo pypy -m pip install --editable .[devel]
    pypy runner --server-host 127.0.0.1:8080 --defaults
    /root/go/bin/hey -n 1000 -c 1 http://127.0.0.1:8080/api/snippy/rest/snippets?limit=20
    /root/go/bin/hey -n 1000 -c 1 http://127.0.0.1:8080/api/snippy/rest/snippets?limit=20
    /root/go/bin/hey -n 1000 -c 1 http://127.0.0.1:8080/api/snippy/rest/snippets?limit=20
    /root/go/bin/hey -n 1000 -c 1 http://127.0.0.1:8080/api/snippy/rest/snippets?limit=20
    /root/go/bin/hey -n 1000 -c 1 http://127.0.0.1:8080/api/snippy/rest/snippets?limit=20
    /root/go/bin/hey -n 10000 -c 1 http://127.0.0.1:8080/api/snippy/rest/snippets?limit=20
    /root/go/bin/hey -n 10000 -c 1 http://127.0.0.1:8080/api/snippy/rest/snippets?limit=20

    Summary:
      Total:        21.4936 secs
      Slowest:      0.0139 secs
      Fastest:      0.0017 secs
      Average:      0.0021 secs
      Requests/sec: 465.2553

      Total data:   319140000 bytes
      Size/request: 31914 bytes

    Response time histogram:
      0.002 [1]     |
      0.003 [9489]  |
      0.004 [204]   |
      0.005 [77]    |
      0.007 [1]     |
      0.008 [146]   |
      0.009 [77]    |
      0.010 [2]     |
      0.011 [2]     |
      0.013 [0]     |
      0.014 [1]     |


    Latency distribution:
      10% in 0.0018 secs
      25% in 0.0019 secs
      50% in 0.0020 secs
      75% in 0.0020 secs
      90% in 0.0021 secs
      95% in 0.0029 secs
      99% in 0.0071 secs

    Details (average, fastest, slowest):
      DNS+dialup:   0.0001 secs, 0.0017 secs, 0.0139 secs
      DNS-lookup:   0.0000 secs, 0.0000 secs, 0.0000 secs
      req write:    0.0000 secs, 0.0000 secs, 0.0002 secs
      resp wait:    0.0020 secs, 0.0016 secs, 0.0127 secs
      resp read:    0.0000 secs, 0.0000 secs, 0.0004 secs

    Status code distribution:
      [200] 10000 responses

    # HTTPS server with PyPy and Sqlite as storage backed (comment psycopg2 out from setup)
    pypy runner --server-host 127.0.0.1:8080 --server-ssl-cert ./server.crt --server-ssl-key ./server.key --defaults
    /root/go/bin/hey -n 1000 -c 1 https://127.0.0.1:8080/api/snippy/rest/snippets?limit=20
    /root/go/bin/hey -n 1000 -c 1 https://127.0.0.1:8080/api/snippy/rest/snippets?limit=20
    /root/go/bin/hey -n 1000 -c 1 https://127.0.0.1:8080/api/snippy/rest/snippets?limit=20
    /root/go/bin/hey -n 1000 -c 1 https://127.0.0.1:8080/api/snippy/rest/snippets?limit=20
    /root/go/bin/hey -n 1000 -c 1 https://127.0.0.1:8080/api/snippy/rest/snippets?limit=20
    /root/go/bin/hey -n 10000 -c 1 https://127.0.0.1:8080/api/snippy/rest/snippets?limit=20

    Summary:
      Total:        108.0445 secs
      Slowest:      0.0409 secs
      Fastest:      0.0075 secs
      Average:      0.0108 secs
      Requests/sec: 92.5545

      Total data:   319140000 bytes
      Size/request: 31914 bytes

    Response time histogram:
      0.008 [1]     |
      0.011 [7368]  |
      0.014 [513]   |
      0.018 [721]   |
      0.021 [8]     |
      0.024 [1377]  |
      0.028 [9]     |
      0.031 [1]     |
      0.034 [0]     |
      0.038 [1]     |
      0.041 [1]     |


    Latency distribution:
      10% in 0.0078 secs
      25% in 0.0079 secs
      50% in 0.0081 secs
      75% in 0.0138 secs
      90% in 0.0215 secs
      95% in 0.0217 secs
      99% in 0.0226 secs

    Details (average, fastest, slowest):
      DNS+dialup:   0.0067 secs, 0.0075 secs, 0.0409 secs
      DNS-lookup:   0.0000 secs, 0.0000 secs, 0.0000 secs
      req write:    0.0000 secs, 0.0000 secs, 0.0002 secs
      resp wait:    0.0039 secs, 0.0021 secs, 0.0180 secs
      resp read:    0.0001 secs, 0.0001 secs, 0.0007 secs

    Status code distribution:
      [200] 10000 responses


.. code:: bash

    # Bench POST with ab.
    {"data":[{"type":"snippet","attributes":{"data":["docker rm $(docker ps --all -q -f status=exited)"],"brief":"testing performance","name":"testing performance","groups":["default"],"tags":["test","performance"],"links":["https://jsonlint.com/"],"versions":["ab==1.0"],"filename":"ab.txt"}}]}
    ab -p snippet.txt -T application/vnd.api+json -c 1 -n 1000 http://127.0.0.1:8080/api/snippy/rest/snippets

    # Bench POST with hey.
    /root/go/bin/hey -m POST -T application/vnd.api+json -D snippet.txt -n 1000 -c 1 http://127.0.0.1:8080/api/snippy/rest/snippets?limit=20

    Summary:
      Total:        2.8403 secs
      Slowest:      0.0255 secs
      Fastest:      0.0027 secs
      Average:      0.0028 secs
      Requests/sec: 352.0781

      Total data:   494000 bytes
      Size/request: 494 bytes

    Response time histogram:
      0.003 [1]     |
      0.005 [994]   |
      0.007 [3]     |
      0.010 [0]     |
      0.012 [0]     |
      0.014 [0]     |
      0.016 [0]     |
      0.019 [0]     |
      0.021 [1]     |
      0.023 [0]     |
      0.025 [1]     |


    Latency distribution:
      10% in 0.0027 secs
      25% in 0.0027 secs
      50% in 0.0028 secs
      75% in 0.0028 secs
      90% in 0.0029 secs
      95% in 0.0030 secs
      99% in 0.0035 secs

    Details (average, fastest, slowest):
      DNS+dialup:   0.0001 secs, 0.0027 secs, 0.0255 secs
      DNS-lookup:   0.0000 secs, 0.0000 secs, 0.0000 secs
      req write:    0.0000 secs, 0.0000 secs, 0.0002 secs
      resp wait:    0.0027 secs, 0.0026 secs, 0.0246 secs
      resp read:    0.0000 secs, 0.0000 secs, 0.0003 secs

    Status code distribution:
      [409] 1000 responses

    /root/go/bin/hey -m POST -T application/vnd.api+json -D snippet.txt -n 1000 -c 1 http://127.0.0.1:8080/api/snippy/rest/snippets?limit=20

    Summary:
      Total:        2.8316 secs
      Slowest:      0.0184 secs
      Fastest:      0.0027 secs
      Average:      0.0028 secs
      Requests/sec: 353.1552

      Total data:   494000 bytes
      Size/request: 494 bytes

    Response time histogram:
      0.003 [1]     |
      0.004 [987]   |
      0.006 [9]     |
      0.007 [0]     |
      0.009 [0]     |
      0.011 [2]     |
      0.012 [0]     |
      0.014 [0]     |
      0.015 [0]     |
      0.017 [0]     |
      0.018 [1]     |


    Latency distribution:
      10% in 0.0027 secs
      25% in 0.0027 secs
      50% in 0.0028 secs
      75% in 0.0028 secs
      90% in 0.0029 secs
      95% in 0.0030 secs
      99% in 0.0045 secs

    Details (average, fastest, slowest):
      DNS+dialup:   0.0001 secs, 0.0027 secs, 0.0184 secs
      DNS-lookup:   0.0000 secs, 0.0000 secs, 0.0000 secs
      req write:    0.0000 secs, 0.0000 secs, 0.0003 secs
      resp wait:    0.0027 secs, 0.0025 secs, 0.0167 secs
      resp read:    0.0000 secs, 0.0000 secs, 0.0003 secs

    Status code distribution:
      [409] 1000 responses

