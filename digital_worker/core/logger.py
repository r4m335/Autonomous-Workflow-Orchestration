import logging
import json
import sys
from datetime import datetime
from typing import Any, Dict

class StructuredLogger:
    def __init__(self, name: str = "digital_worker"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Avoid duplicate handlers
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            self.logger.addHandler(handler)

    def _log(self, level: int, message: str, thread_id: str = "N/A", **kwargs):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": logging.getLevelName(level),
            "thread_id": thread_id,
            "message": message,
            **kwargs
        }
        self.logger.log(level, json.dumps(log_entry))

    def info(self, message: str, thread_id: str = "N/A", **kwargs):
        self._log(logging.INFO, message, thread_id, **kwargs)

    def error(self, message: str, thread_id: str = "N/A", **kwargs):
        self._log(logging.ERROR, message, thread_id, **kwargs)

    def warning(self, message: str, thread_id: str = "N/A", **kwargs):
        self._log(logging.WARNING, message, thread_id, **kwargs)

logger = StructuredLogger()
