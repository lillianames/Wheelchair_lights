from flask import Flask, render_template
from flask_socketio import SocketIO
import threading
import time
import random
from rpi_ws281x import PixelStrip, Color

# Initialize Flask app and SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

# LED Setup
NUM_PIXELS = 32  # Adjust for your LED HAT
LED_PIN = 18
strip = PixelStrip(NUM_PIXELS, LED_PIN)
strip.begin()

# Brightness Levels
BRIGHTNESS_LEVELS = [0, 1, 50, 100, 150, 200, 250]
brightness = 100  # Default medium brightness

# Dictionary to track active patterns
active_patterns = {
    "solid_red": False,
    "blinking_orange": False,
    "right_turn": False,
    "left_turn": False,
    "rainbow": False,
    "fireworks": False
}

def scale_color(r, g, b):
    """Scale color brightness based on the global brightness value."""
    scale_factor = brightness / 250  # Scale brightness within range
    return Color(int(r * scale_factor), int(g * scale_factor), int(b * scale_factor))

def clear():
    """Turn off all LEDs."""
    for i in range(NUM_PIXELS):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

def solid_red():
    """Turn all LEDs solid red."""
    while active_patterns["solid_red"]:
        for i in range(NUM_PIXELS):
            strip.setPixelColor(i, scale_color(255, 0, 0))  # Red
        strip.show()
        time.sleep(0.1)

def blinking_orange():
    """Blink all LEDs orange."""
    while active_patterns["blinking_orange"]:
        for i in range(NUM_PIXELS):
            strip.setPixelColor(i, scale_color(255, 165, 0))  # Orange
        strip.show()
        time.sleep(0.5)
        clear()
        time.sleep(0.5)

def right_turn():
    """Blink the right side of the grid in GREEN."""
    while active_patterns["right_turn"]:
        for row in range(8):
            for col in range(4, 8):  # Right half
                led_index = row * 8 + col
                if 0 <= led_index < NUM_PIXELS:
                    strip.setPixelColor(led_index, scale_color(0, 255, 0))  # Green
        strip.show()
        time.sleep(0.5)
        clear()
        time.sleep(0.5)

def left_turn():
    """Blink the left side of the grid in BLUE."""
    while active_patterns["left_turn"]:
        for row in range(8):
            for col in range(4):  # Left half
                led_index = row * 8 + col
                if 0 <= led_index < NUM_PIXELS:
                    strip.setPixelColor(led_index, scale_color(0, 0, 255))  # Blue
        strip.show()
        time.sleep(0.5)
        clear()
        time.sleep(0.5)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions with brightness scaling."""
    if pos < 85:
        return scale_color(pos * 3, 255 - pos * 3, 0)  # Red → Green
    elif pos < 170:
        pos -= 85
        return scale_color(255 - pos * 3, 0, pos * 3)  # Green → Blue
    else:
        pos -= 170
        return scale_color(0, pos * 3, 255 - pos * 3)  # Blue → Red

def rainbow():
    """Display a rainbow cycle across all LEDs."""
    offset = 0
    while active_patterns["rainbow"]:
        for i in range(NUM_PIXELS):
            wheel_pos = (i + offset) % 256
            strip.setPixelColor(i, wheel(wheel_pos))
        strip.show()
        time.sleep(0.1)
        offset += 2

def fireworks():
    """Simulate a fireworks display with bursts."""
    while active_patterns["fireworks"]:
        num_bursts = random.randint(4, 7)  

        for _ in range(num_bursts):
            if not active_patterns["fireworks"]:
                clear()
                return

            row = random.randint(0, 7)  # 8 rows (0-7)
            burst_size = random.randint(2, 5)
            start_col = random.randint(0, 8 - burst_size)
            color = random.choice([(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0)])

            for i in range(burst_size):
                if not active_patterns["fireworks"]:
                    clear()
                    return
                led_index = row * 8 + (start_col + i)
                strip.setPixelColor(led_index, scale_color(*color))
            strip.show()
            time.sleep(0.03)

            for fade in range(7, 0, -1):
                if not active_patterns["fireworks"]:
                    clear()
                    return
                fade_factor = fade / 7
                for i in range(burst_size):
                    led_index = row * 8 + (start_col + i)
                    strip.setPixelColor(led_index, scale_color(
                        int(color[0] * fade_factor),
                        int(color[1] * fade_factor),
                        int(color[2] * fade_factor)
                    ))
                strip.show()
                time.sleep(0.02)

        for _ in range(int(random.uniform(3, 7) * 10)):
            if not active_patterns["fireworks"]:
                clear()
                return
            time.sleep(0.03)

def toggle_pattern(pattern_name, function):
    """Toggles LED patterns on/off."""
    if active_patterns[pattern_name]:
        active_patterns[pattern_name] = False
        clear()
    else:
        active_patterns.update({key: False for key in active_patterns})  # Turn off other patterns
        active_patterns[pattern_name] = True
        threading.Thread(target=function, daemon=True).start()

# Web routes
@app.route('/')
def index():
    return render_template('index.html')

# SocketIO events for patterns
@socketio.on('solid_red')
def handle_solid_red():
    toggle_pattern("solid_red", solid_red)

@socketio.on('blinking_orange')
def handle_blinking_orange():
    toggle_pattern("blinking_orange", blinking_orange)

@socketio.on('right_turn')
def handle_right_turn():
    toggle_pattern("right_turn", right_turn)

@socketio.on('left_turn')
def handle_left_turn():
    toggle_pattern("left_turn", left_turn)

@socketio.on('rainbow')
def handle_rainbow():
    toggle_pattern("rainbow", rainbow)

@socketio.on('fireworks')
def handle_fireworks():
    toggle_pattern("fireworks", fireworks)

# Brightness Control
@socketio.on('set_brightness')
def set_brightness(data):
    """Set brightness to a fixed level."""
    global brightness
    if data["brightness"] in BRIGHTNESS_LEVELS:
        brightness = data["brightness"]
        socketio.emit('brightness_update', {'brightness': brightness})
        apply_brightness_update()

def apply_brightness_update():
    """Update the currently active pattern to reflect brightness changes."""
    for pattern, is_active in active_patterns.items():
        if is_active:
            threading.Thread(target=globals()[pattern], daemon=True).start()
            break

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)
