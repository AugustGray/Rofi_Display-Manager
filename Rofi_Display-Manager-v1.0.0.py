from pathlib import Path
import subprocess

def rofi_menu(prompt, options, placeholder="Select an option"):
    """Displays a rofi menu with a custom placeholder text."""
    menu = "\n".join(options) if options else ""
    result = subprocess.run(
        ["rofi", "-dmenu", "-p", prompt, "-mesg", placeholder, "-theme", str(Path(__file__).parent / "theme/launcher.rasi")],
        input=menu, text=True, capture_output=True
    ).stdout.strip()
    return result

def disconnect_display():
    choice = rofi_menu("Disconnect Display", ["Default (HDMI-A-0)", "Custom Display"], "Select an option")
    
    if choice == "Default (HDMI-A-0)":
        command = ["xrandr", "--output", "HDMI-A-0", "--off"]
    elif choice == "Custom Display":
        custom_display = rofi_menu("Type display name to disconnect:", [], "Type display name here...")
        command = ["xrandr", "--output", custom_display, "--off"]
    else:
        return
    
    subprocess.run(command)

def select_resolution(display):
    choice = rofi_menu("Select Resolution", ["Auto (Default)", "Custom Resolution"], "Select an option")
    if choice == "Custom Resolution":
        resolution = rofi_menu("Enter resolution (e.g., 1920x1080):", [], "Type resolution here...")
        if resolution:
            return ["--mode", resolution]
    return []

def connect_display():
    choice = rofi_menu("Connect Display", ["Mirror Screen (Default)", "Extend to Left", "Extend to Right", "Custom Display"], "Select an option")
    
    if choice == "Mirror Screen (Default)":
        resolution_flags = select_resolution("HDMI-A-0")
        command = ["xrandr", "--output", "HDMI-A-0", "--auto"] + resolution_flags
    elif choice in ["Extend to Left", "Extend to Right"]:
        direction = "left" if "Left" in choice else "right"
        command = ["xrandr", "--output", "HDMI-A-0", "--auto", f"--{direction}-of", "eDP"]
    elif choice == "Custom Display":
        custom_display = rofi_menu("Type new display name:", [], "Type display name here...")
        connected_display = rofi_menu("Type already connected display name (default: eDP):", [], "Type connected display name...") or "eDP"
        position = rofi_menu("Mirror or Extend?", ["Mirror", "Extend to Left", "Extend to Right"], "Select an option")
        
        if position == "Mirror":
            resolution_flags = select_resolution(custom_display)
            command = ["xrandr", "--output", custom_display, "--auto"] + resolution_flags
        elif position in ["Extend to Left", "Extend to Right"]:
            direction = "left" if "Left" in position else "right"
            command = ["xrandr", "--output", custom_display, "--auto", f"--{direction}-of", connected_display]
        else:
            return
    else:
        return
    
    subprocess.run(command)

def main():
    choice = rofi_menu("Display Manager", ["Connect Display", "Disconnect Display"], "Select an option")
    
    if choice == "Connect Display":
        connect_display()
    elif choice == "Disconnect Display":
        disconnect_display()

if __name__ == "__main__":
    main()