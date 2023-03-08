import time
import pychromecast
import zeroconf


def get_volume(cast):
    return cast.status.volume_level


def set_volume(cast, volume):
    cast.set_volume(volume)
    print(f"Volume set to {volume}.")


def monitor_volume(cast, target_volume):
    while True:
        time.sleep(3)
        current_volume = get_volume(cast)
        print(f"Current volume level: {current_volume}")
        if current_volume > target_volume:
            set_volume(cast, target_volume)


while True:
    try:
        zconf = zeroconf.Zeroconf()
        browser = pychromecast.CastBrowser(
            pychromecast.SimpleCastListener(lambda uuid, service: print(browser.devices[uuid].friendly_name)), zconf)
        browser.start_discovery()

        chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=["Sala de jantar"])
        if not chromecasts:
            raise Exception("No Chromecast devices found with the specified friendly name.")

        cast = chromecasts[0]
        cast.wait()

        target_volume = 0.39

        # Get the current volume
        current_volume = get_volume(cast)
        # print(f"Current volume level: {current_volume}")
        # Start monitoring the volume
        monitor_volume(cast, target_volume)

    except pychromecast.error.ChromecastConnectionError as e:
        print(f"Chromecast connection error: {e}")
        print("Retrying in 5 seconds...")
        time.sleep(5)

    except zeroconf.NonUniqueNameException as e:
        print(f"Zeroconf error: {e}")
        print("Retrying in 5 seconds...")
        time.sleep(5)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print("Retrying in 5 seconds...")
        time.sleep(5)
