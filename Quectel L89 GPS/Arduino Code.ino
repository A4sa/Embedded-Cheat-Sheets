#include <SoftwareSerial.h> // Include the SoftwareSerial library
#define ARDUINO_GPS_RX 9 // Arduino RX pin connected to GPS TX
#define ARDUINO_GPS_TX 8 // Arduino TX pin connected to GPS RX
#define GPS_BAUD_RATE 9600 // The GPS Shield module defaults to 9600 baud
// Create a SoftwareSerial object called gps:
SoftwareSerial gpsPort(ARDUINO_GPS_TX, ARDUINO_GPS_RX);

// This is the hardware serial port on pins 0/1.
#define SerialMonitor Serial

void setup()
{
gpsPort.begin(GPS_BAUD_RATE);
SerialMonitor.begin(9600);
}

void loop()
{
if (gpsPort.available()) // If GPS data is available
SerialMonitor.write(gpsPort.read()); // Read it and print to SerialMonitor
if (SerialMonitor.available()) // If SerialMonitor data is available
gpsPort.write(SerialMonitor.read()); // Read it and send to GPS
}
