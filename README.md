# mega_scheduler
### Environment
```bash
EMAIL=xxx
PASSWORD=xxx
TARGET_DIR=/path/to/dir
BACKUP_TIME=04:00
```

### docker-compose.yml
```yaml
  mega_scheduler:
    image: ghcr.io/ejach/mega_scheduler:latest
    container_name: mega_scheduler
    environment:
      - EMAIL=${EMAIL}
      - PASSWORD=${PASSWORD}
      - TARGET_DIR=${TARGET_DIR}
      - BACKUP_TIME=${BACKUP_TIME}
    volumes:
      - ${TARGET_DIR}:/${TARGET_DIR}
    restart: unless-stopped
```

