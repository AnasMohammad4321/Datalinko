import sys
import os
import logging


app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'app'))
sys.path.append(app_path)

from app.app import app


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)


def get_available_port(start_port=8060):
    import socket
    port = start_port
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                logger.debug(f"Found available port: {port}")
                return port
        except OSError:
            logger.debug(f"Port {port} is in use, trying next port")
            port += 1

if __name__ == "__main__":
    port = get_available_port()
    logger.info(f"Starting server on port {port}")
    logger.info("Debug mode is enabled")
    app.run_server(debug=True, port=port)
