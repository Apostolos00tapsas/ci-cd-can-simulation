import can
import time
import logging
import warnings

warnings.filterwarnings("ignore")

# Ρύθμιση logging
logging.basicConfig(
    filename="can_logs.log",  # Saves logs in a file
    level=logging.INFO,  
    format="%(asctime)s [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def setup_can_bus():
    bus = can.Bus(
        interface="virtual",
        channel=0,  
        receive_own_messages=True  # It allows to read what sends.
    )
    logging.info("✅ CAN Bus initialized (Virtual, Channel 0)")
    return bus

def send_can_message(bus, arbitration_id, data):
    message = can.Message(arbitration_id=arbitration_id, data=data, is_extended_id=False)
    bus.send(message)
    logging.info(f"📤 Sent CAN Bus message: ID={hex(arbitration_id)}, Data={data}")

def receive_can_message(bus, timeout=1.0):
    message = bus.recv(timeout)
    if message:
        logging.info(f"📥 Received CAN Bus message: ID={hex(message.arbitration_id)}, Data={message.data}")
        return message
    else:
        logging.warning("⏳ No Response from CAN Bus.")
        return None

if __name__ == "__main__":
    bus = setup_can_bus()
    send_can_message(bus, 0x123, [0x11, 0x22, 0x33])
    time.sleep(1)
    receive_can_message(bus)
    bus.shutdown()
    logging.info("✅ VirtualBus shutdown successfully.")
