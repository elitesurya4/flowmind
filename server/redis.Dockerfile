FROM redis:7.2-alpine

EXPOSE 6379

CMD ["redis-server", "--appendonly", "yes", "--appendfsync", "everysec", "--save", "60", "1"]