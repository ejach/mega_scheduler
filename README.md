# megaUploadScheduler
### Environment
```bash
EMAIL=xxx
PASSWORD=xxx
TARGET_DIR=/mnt/hdd
BACKUP_TIME=04:00
```

### docker-compose.yml
```yaml
  mega_upload:
    image: ejach/mega_upload:latest
    container_name: mega_upload
    environment:
      - EMAIL=${EMAIL}
      - PASSWORD=${PASSWORD}
      - TARGET_DIR=${TARGET_DIR}
      - BACKUP_TIME=${BACKUP_TIME}
    volumes:
      - ${TARGET_DIR}:/${TARGET_DIR}
    restart: unless-stopped
```

