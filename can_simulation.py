import can
import cantools
import time
import logging
import warnings
from can.message import Message

warnings.filterwarnings("ignore")

# Ρύθμιση logging
logging.basicConfig(
    filename="can_logs.log",  # Saves logs in a file
    level=logging.INFO,  
    format="%(asctime)s [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Φόρτωση του DBC αρχείου
def load_dbc(dbc_path):
    """Load the DBC file."""
    try:
        db = cantools.database.load_file(dbc_path)
        return db
    except Exception as e:
        raise ValueError(f"Error loading DBC file: {e}")

# Δημιουργία CAN Bus interface
def setup_can_bus():
    bus = can.Bus(interface="virtual", channel=0, receive_own_messages=True)
    return bus

# Αποστολή CAN μηνύματος
def send_can_message(bus, arbitration_id, data):
    message = can.Message(arbitration_id=arbitration_id, data=data, is_extended_id=False)
    bus.send(message)
    print(f"📤 Send CAN Bus message: ID={hex(arbitration_id)}, Data={data}")

def receive_can_message(bus, timeout=1.0):
    message = bus.recv(timeout)
    if message:
        logging.info(f"📥 Received CAN Bus message: ID={hex(message.arbitration_id)}, Data={message.data}")
        return message
    else:
        logging.warning("⏳ No Response from CAN Bus.")
        return None
    
# Manually call the function with the mocked message
def test_receive_can_message(mock_message, dbc):
    """Test function that processes a mocked CAN message."""
    print(f"📥 Mocked CAN Message for dbc file: ID={hex(mock_message.arbitration_id)}, Raw Data={mock_message.data.hex()}")
    
    try:
        decoded = dbc.decode_message(mock_message.arbitration_id, mock_message.data)
        print("🔍 Decoded Signals:")
        for signal, value in decoded.items():
            print(f"   - {signal}: {value}")
    except Exception as e:
        print(f"⚠️ Decoding Failed: {e}")


if __name__ == "__main__":
    dbc_path = "CSS-Electronics-OBD2-v1.4.dbc"  # Βάλε το path του .dbc αρχείου σου
    dbc = load_dbc(dbc_path)
    bus = setup_can_bus()
    send_can_message(bus, 0x123, [0x11, 0x22, 0x33])
    time.sleep(1)
    bus.shutdown()
    print("✅ VirtualBus shutdown successfully.")
    # Simulate a CAN message with an ID and raw data
    mock_message = Message(
    arbitration_id=0x7E8,  # ✅ Use the correct ID from the DBC file
    data=bytes([
        225,  # Example: S1_PID_64_EngPctTorq_EP4 (Raw: 225 → Decoded: 225 - 125 = 100%)
        150,  # Example: S1_PID_65_AuxInputOutput (Raw: 150 → Decoded: 150)
        90,   # Example: S1_PID_67_EngineCoolantTemp (Raw: 90 → Decoded: 90°C)
        240,  # Example: S1_PID_8E_EngFrictionPctTorq (Raw: 240 → Decoded: 240 - 125 = 115%)
        0, 0, 0, 0  # Padding (8-byte message required)
    ]),
    is_extended_id=False
    )
    #Run the test with the mocked message
    test_receive_can_message(mock_message, dbc)
    

    