FROM alpine:3.19

RUN apk add --no-cache redis socat

# HTTP responder for Render
RUN printf '#!/bin/sh\nprintf "HTTP/1.1 200 OK\r\nContent-Length:2\r\n\r\nOK"' > /health && chmod +x /health

CMD ["sh", "-c", "redis-server --appendonly yes --appendfsync everysec --save 60 1 & socat TCP-LISTEN:80,fork EXEC:/health & wait"]