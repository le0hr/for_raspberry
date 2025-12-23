# ⚡ Raspberry Pi Power Outage Clock (ST7789)

An **embedded Raspberry Pi project** that displays the remaining time until a **scheduled power outage** based on messages received via **Telegram**, using an **ST7789 SPI LCD display**.

Designed for **Raspberry Pi Zero 1**, this project combines hardware interfacing, asynchronous Python logic, and message parsing to provide real-time, offline-visible information during power instability.

---

## 🧠 Project Overview

This system monitors Telegram messages from a predefined source (e.g. an official channel or bot) and extracts power outage schedules using configurable patterns.
The parsed data is then visualized on a **ST7789 LCD display**, showing **how much time remains until electricity is cut off in a specific area**.

The project is especially useful in regions with **scheduled or rotating power outages**, where quick visual access to timing information is critical.

---

## 🧰 Hardware Requirements

* **Raspberry Pi Zero 1**
* **ST7789 LCD display**

  * Interface: **SPI**
* Stable 3.3V power supply
* SPI-enabled Raspberry Pi OS

---

## 🧪 Software Stack

* **Python 3**
* **asyncio**
* **luma.lcd** (ST7789 driver)
* **pillow**
* **Telegram API** (via `api_id` and `api_hash`)
* **Raspberry Pi OS** (Lite recommended)

---

## 📟 Display Functionality

The LCD screen shows:

* ⏳ **Remaining time until power outage**
* 🕒 Time is updated dynamically
* 📉 Countdown adapts based on the latest known outage schedule

The display is designed to be:

* minimalistic
* readable at a distance
* energy efficient
* reliable even with limited system resources (Pi Zero)


---

## ⚙️ Configuration File

The project uses a **configuration file** (e.g. `config.cfg`) that allows full customization without changing the code.

### Configurable parameters include:

* **Telegram API credentials**

  * `api_id`
  * `api_hash`
* **Message source**

  * Channel / chat ID or username
* **Message pattern**

  * Regex or keyword pattern to extract outage times
* **Power outage queue**

  * Rotation / schedule index for the selected area
* **Region-specific settings**

  * Area or district identifier

> This design allows the same codebase to be reused for different regions, schedules, or message formats.

---

## 🚀 How It Works

1. The application connects to Telegram using provided API credentials
2. It listens to messages from a configured source
3. Messages are parsed using a user-defined pattern
4. The power outage schedule is extracted
5. Remaining time is calculated
6. The countdown is rendered on the ST7789 display

All logic runs asynchronously to remain responsive on **low-power hardware**.

---

## 📁 Project Structure

```
raspberry_clock/
├── main.py              # Application entry point
├── display.py           # ST7789 display logic (luma.lcd)
├── message_handler.py   # Telegram message parsing
├── config.cfg           # User configuration (not committed)
├── requirements.txt
└── README.md
```

---

## 🚧 Project Status

**Work in Progress**

Planned improvements:

* Better error handling for malformed messages
* Display layout customization
* Support for multiple outage schedules
* Optional fallback logic when Telegram is unavailable

---

## 💡 Use Cases

* Embedded systems portfolio project
* Raspberry Pi + LCD experimentation
* Power outage monitoring
* Smart home / automation dashboards
* Asynchronous Python on constrained hardware

---

## ⚠️ Notes

* SPI must be enabled in `raspi-config`
* Designed and tested for **Raspberry Pi Zero 1**

---

## 👤 Author

Developed as an **embedded & automation-focused project** for learning and portfolio purposes.

---