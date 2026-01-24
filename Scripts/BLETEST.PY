import asyncio
from bleak import BleakScanner, BleakClient

# Replace this with the ID you found (MAC address or UUID)
ADDRESS = "1C:DB:D4:AE:D4:F5"

async def run_scanner():
    print("Scanning for devices...")
    # This will scan for 5 seconds by default
    devices = await BleakScanner.discover()
    
    for d in devices:
        # 'd.address' is the MAC (Win/Linux) or UUID (macOS)
        # 'd.name' is the name the device is broadcasting
        print(f"Device: {d.name} | ID: {d.address}")

async def connect_to_device():
    print(f"Connecting to {ADDRESS}...")
    
    # Using 'async with' ensures the connection closes automatically when done
    async with BleakClient(ADDRESS) as client:
        if client.is_connected:
            print("Successfully connected! ✅")
            
            # This lists everything the device can do
            for service in client.services:
                print(f"\nService: {service}")
                for char in service.characteristics:
                    print(f"  - Characteristic: {char.uuid} ({','.join(char.properties)})")
            
            await client.write_gatt_char("beb5483e-36e1-4688-b7f5-ea07361b26a8", "0".encode())
            print(f"sent a value over to MC\n")

        else:
            print("Failed to connect. ❌")
        await client.disconnect()
        print("Disconnected from Client\n")
    
if __name__ == "__main__":
    asyncio.run(connect_to_device())