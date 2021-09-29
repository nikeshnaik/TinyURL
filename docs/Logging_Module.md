Logging Module

# Logging Design Doc

### Requirements

#### Functional

- Log each request
- centralized logging with ELK stack
- use filebeat to read logs from all microservices
- use APM to monitor logs
- use Obserevlibility to check patterns in logs and metrics 

#### Non-Functional

- Logging shouldn't affect latency
- Logging must be simple to use and extendable
- Must replace print statement.
- Use Configuration file to setup logging

### Technical Plan

- Use Logging std module from python
- Use FileHandler to write logs to a logfiles.
- Rotate FileHandler logs
- Use error loglevel for produciton
- During local development, tail the log file to check logs
- Use Formatter: '%(message)%(levelname)%(name)%(asctime)%(module)%(funcName)%(pathname)%(lineno)%(filename)'
- Add log file to .gitignore
- Filebeat will read from log file and store in ELK Stack

#### Logging Config
```
version: 1
formatters:
  default:
    format: '%(message)%(levelname)%(name)%(asctime)%(module)%(funcName)%(pathname)%(lineno)%(filename)'
    class: pythonjsonlogger.jsonlogger.JsonFormatter
handlers:
  console:
    class: logging.StreamHandler
    level: INFO
    formatter: default
    stream: ext://sys.stdout
  file:
    class: logging.handlers.TimedRotatingFileHandler
    level: ERROR
    formatter: default
    filename: turl.log
    backupCount: 4
loggers:
  local:
    handlers: [console]
    propagate: True
  prod:
    handlers: [file]
    propagate: False
root:
  level: DEBUG
  handlers: [console, file]
```

- Use only one logger for whole app turl
- Change Logger based on env set by in .env
