#!/usr/bin/env python3

import asyncio
from mavsdk import System
from mavsdk.geofence import Point, Polygon

"""
This example shows how to use the geofence plugin.
Note: The behavior when your vehicle hits the geofence is NOT configured
in this example.
"""


async def run():

    # Connect to the Simulation
    drone = System()
    await drone.connect(system_address="udp://:14540")

    # Wait for the drone to connect
    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    # Fetch the home location coordinates, in order to set a boundary around
    # the home location.
   # print("Fetching home location coordinates...")
    #async for terrain_info in drone.telemetry.home():
       # latitude = terrain_info.latitude_deg
       # longitude = terrain_info.longitude_deg
       # break

    await asyncio.sleep(1)

    # Define your geofence boundary
    file = open('coords.txt', 'r')
    fence = []
    for line in file:
        m = line.split(',')
        fence.append(Point(float(m[0]), float(m[1].strip())))

    # Create a polygon object using your points
    polygon = Polygon(fence, Polygon.FenceType.INCLUSION)

    # Upload the geofence to your vehicle
    print("Uploading geofence...")
    await drone.geofence.upload_geofence([polygon])

    print("Geofence uploaded!")


if __name__ == "__main__":
    # Run the asyncio loop
    asyncio.run(run())