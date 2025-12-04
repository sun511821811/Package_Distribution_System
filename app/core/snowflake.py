import time
import logging

logger = logging.getLogger(__name__)

class SnowflakeGenerator:
    def __init__(self, datacenter_id: int, worker_id: int, sequence: int = 0):
        """
        Snowflake ID Generator
        :param datacenter_id: Data center ID (0-31)
        :param worker_id: Worker ID (0-31)
        :param sequence: Initial sequence (0-4095)
        """
        self.worker_id_bits = 5
        self.datacenter_id_bits = 5
        self.max_worker_id = -1 ^ (-1 << self.worker_id_bits)
        self.max_datacenter_id = -1 ^ (-1 << self.datacenter_id_bits)
        
        self.sequence_bits = 12
        self.worker_id_shift = self.sequence_bits
        self.datacenter_id_shift = self.sequence_bits + self.worker_id_bits
        self.timestamp_left_shift = self.sequence_bits + self.worker_id_bits + self.datacenter_id_bits
        
        self.sequence_mask = -1 ^ (-1 << self.sequence_bits)
        
        # Epoch: 2024-01-01 00:00:00 UTC
        self.twepoch = 1704067200000

        if worker_id > self.max_worker_id or worker_id < 0:
            raise ValueError(f"Worker ID must be between 0 and {self.max_worker_id}")
        if datacenter_id > self.max_datacenter_id or datacenter_id < 0:
            raise ValueError(f"Datacenter ID must be between 0 and {self.max_datacenter_id}")

        self.worker_id = worker_id
        self.datacenter_id = datacenter_id
        self.sequence = sequence
        self.last_timestamp = -1

    def _gen_timestamp(self):
        return int(time.time() * 1000)

    def _til_next_millis(self, last_timestamp):
        timestamp = self._gen_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._gen_timestamp()
        return timestamp

    def next_id(self) -> int:
        timestamp = self._gen_timestamp()

        if timestamp < self.last_timestamp:
            logger.error(f"Clock moved backwards. Refusing to generate id for {self.last_timestamp - timestamp} milliseconds")
            raise Exception("Clock moved backwards")

        if self.last_timestamp == timestamp:
            self.sequence = (self.sequence + 1) & self.sequence_mask
            if self.sequence == 0:
                timestamp = self._til_next_millis(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        new_id = ((timestamp - self.twepoch) << self.timestamp_left_shift) | \
                 (self.datacenter_id << self.datacenter_id_shift) | \
                 (self.worker_id << self.worker_id_shift) | \
                 self.sequence
        return new_id

# Global instance
# In a real distributed system, these should be configured per instance
snowflake = SnowflakeGenerator(datacenter_id=1, worker_id=1)
