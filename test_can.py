import pytest
import time
from can_simulation import setup_can_bus, send_can_message, receive_can_message
import warnings
warnings.filterwarnings("ignore")

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

bus = setup_can_bus()
print("CAN Bus initialized:", bus)
bus.shutdown()  # Κλείνει σωστά το Virtual CAN Bus πριν το script τελειώσει
print("✅ VirtualBus shutdown successfully.")
