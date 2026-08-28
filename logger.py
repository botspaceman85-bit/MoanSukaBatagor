import logging
import os
from datetime import datetime
from colorama import Fore, Style

class ChaosLogger:
    def __init__(self, name="chaos"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_format)
        self.logger.addHandler(console_handler)
        
        # File handler
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        log_file = f"{log_dir}/chaos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_format)
        self.logger.addHandler(file_handler)
    
    def info(self, msg):
        self.logger.info(f"{Fore.GREEN}{msg}{Style.RESET_ALL}")
    
    def error(self, msg):
        self.logger.error(f"{Fore.RED}{msg}{Style.RESET_ALL}")
    
    def warning(self, msg):
        self.logger.warning(f"{Fore.YELLOW}{msg}{Style.RESET_ALL}")
    
    def debug(self, msg):
        self.logger.debug(msg)
    
    def chaos(self, msg):
        self.logger.info(f"{Fore.MAGENTA}[🔥] {msg}{Style.RESET_ALL}")