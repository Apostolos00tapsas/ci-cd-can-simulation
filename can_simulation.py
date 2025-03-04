import can
import time
import warnings
warnings.filterwarnings("ignore")

def setup_can_bus():
    #Create CAN Bus interface.
    bus = can.Bus(
        interface="virtual",
        channel=0,  
        receive_own_messages=True  # Επιτρέπει να διαβάζει τα μηνύματα που στέλνει
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

if __name__ == "__main__":
    bus = setup_can_bus()
    send_can_message(bus, 0x123, [0x11, 0x22, 0x33])
    time.sleep(1)
    receive_can_message(bus)
    bus.shutdown()  # Κλείνει σωστά το Virtual CAN Bus πριν το script τελειώσει
    print("✅ VirtualBus shutdown successfully.")
