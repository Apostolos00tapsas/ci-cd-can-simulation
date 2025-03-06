import pytest
import time
from can.message import Message
from can_simulation import setup_can_bus, send_can_message, receive_can_message, load_dbc
import warnings
warnings.filterwarnings("ignore")

@pytest.fixture
def dbc():
    """Load the DBC file."""
    # Replace this with the actual method of loading your DBC file
    db = load_dbc('CSS-Electronics-OBD2-v1.4.dbc')
    return db

@pytest.fixture
def can_bus():
    return setup_can_bus()

def test_can_message_exchange(can_bus):
    # Test for send and recieve CAN Messages
    send_can_message(can_bus, 0x123, [0x11, 0x22, 0x33])
    time.sleep(1) # wait 1 sec
    received_message = receive_can_message(can_bus)
    
    assert received_message is not None, "❌ Mesage is not received!"
    assert received_message.arbitration_id == 0x123, "❌ Wrong CAN ID!"
    assert received_message.data == bytearray([0x11, 0x22, 0x33]), "❌ Data missmach!"

"""
def test_receive_can_message(dbc):
    mock_message = Message(
        arbitration_id=0x7E8,  # ✅ Use the correct ID from the DBC file
        data=bytes([           # Example mock data
            225,  # Example: S1_PID_64_EngPctTorq_EP4 (Raw: 225 → Decoded: 225 - 125 = 100%)
            150,  # Example: S1_PID_65_AuxInputOutput (Raw: 150 → Decoded: 150)
            90,   # Example: S1_PID_67_EngineCoolantTemp (Raw: 90 → Decoded: 90°C)
            240,  # Example: S1_PID_8E_EngFrictionPctTorq (Raw: 240 → Decoded: 240 - 125 = 115%)
            0, 0, 0, 0  # Padding (8-byte message required)
        ]),
        is_extended_id=False
    )
    
    try:
        decoded = dbc.decode_message(mock_message.arbitration_id, mock_message.data)
        for signal, value in decoded.items():
            if signal =="- length:":
                assert value == 255 
            if signal =="- response:":
                assert value == 7
    except Exception as e:
        print(f"⚠️ Decoding Failed: {e}")
"""
