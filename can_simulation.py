import can
import warnings
warnings.filterwarnings("ignore")

def setup_can_bus():
    #Create CAN Bus interface.
    bus = can.Bus(
        interface="virtual",
        channel=0,  
        receive_own_messages=True  # It allows to read what sends.
    )
    return bus

def send_can_message(bus, arbitration_id, data):
    #Send a CAN Bus Message
    message = can.Message(arbitration_id=arbitration_id, data=data, is_extended_id=False)
    bus.send(message)
    print(f"📤 Send CAN Bus message: ID={hex(arbitration_id)}, Data={data}")

def receive_can_message(bus, timeout=1.0):
    # Receive CAN Bus Message
    message = bus.recv(timeout)
    if message:
        print(f"📥 Receive CAN Bus Message: ID={hex(message.arbitration_id)}, Data={message.data}")
        return message
    else:
        print("⏳ No Responce from CAN Bus.")
        return None

