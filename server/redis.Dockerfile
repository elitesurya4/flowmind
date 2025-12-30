FROM redis:7.2-alpine

CMD ["redis-server", "--appendonly", "yes", "--appendfsync", "everysec", "--save", "60", "1"]