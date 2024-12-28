//Game boy Printer interface with Arduino, by Caleb Dennis
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// Create an instance of the OLED display
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 32
#define OLED_RESET    -1 // Reset pin not used
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

char byte_read;
bool bit_sent, bit_read;
int clk = 2;   // clock signal
int TX = 3;    // The data signal coming from the Arduino and goind to the printer (Sout on Arduino becomes Sin on the printer)
int RX = 4;    // The response bytes coming from printer going to Arduino (Sout from printer becomes Sin on the Arduino)
int LED = 13;  //to indicate a printer ready state
//invert TX/RX if it does not work, assuming that everything else is OK

// Declare variables for display update timing
unsigned long lastDisplayUpdate = 0; // Timer for display updates
const unsigned long displayUpdateInterval = 200; // Update every 200 ms
bool dataSent = false; // Flag to indicate if data has been sent
bool displayOne = true; // Flag to indicate if sending is displayed 

void setup() {
  // ############################# display code ################################################
  // Initialize the display
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.println("Booting..........");
  display.display();
  delay(1000); // Wait for 1 second

  // ############################## printer code ###############################################
  // Printer pin setup
  pinMode(clk, OUTPUT);
  pinMode(TX, OUTPUT);
  pinMode(LED, OUTPUT);
  pinMode(RX, INPUT_PULLUP);
  digitalWrite(clk, HIGH);
  digitalWrite(TX, LOW);
  Serial.begin(9600); // Start serial communication
  while (!Serial) { ; } // Wait for serial port to connect
  Serial.println("Waiting for data ");
  display.clearDisplay();
  display.setCursor(0, 0);
  display.println("GB Printer READY!");
  display.display();
  while (Serial.available() > 0) {  // Flush the buffer
    Serial.read();
  }
  digitalWrite(LED, HIGH); // Turn on the LED
}

void loop() {
  static unsigned long lastUpdateTime = 0; // Timer for display updates
  const unsigned long displayDuration = 1000; // Duration to show "Sending data..." in milliseconds

  if (Serial.available() > 0) {
    char data = Serial.read(); // Read the incoming byte
    Serial.write(printing(data)); // Send data to the printer
    dataSent = true; // Set the flag indicating data has been sent

    // Update the display to show "Sending data" only once
    if (displayOne) {
      display.clearDisplay();
      display.setCursor(0, 0);
      display.print("Sending data...");
      display.display();
      displayOne = false; // Prevent repeated updates
      lastUpdateTime = millis(); // Record the time of the last update
    }

  } else {
    // If data has been sent, check if we should display "GB Printer READY!"
    if (dataSent) {
      // Check if enough time has passed since the last update
      if (millis() - lastUpdateTime >= displayDuration) {
        display.clearDisplay();
        display.setCursor(0, 0);
        display.println("GB Printer READY!");
        display.display();
        dataSent = false; // Reset the flag
        displayOne = true; // Reset the display flag for the next data send
      }
    }
  }
}

char printing(char byte_sent) {  // this function prints bytes to the serial
  for (int i = 0; i <= 7; i++) {
    bit_sent = bitRead(byte_sent, 7 - i);
    digitalWrite(clk, LOW);
    digitalWrite(TX, bit_sent);
    digitalWrite(LED, bit_sent);
    delayMicroseconds(30);  //double speed mode
    digitalWrite(clk, HIGH);
    bit_read = (digitalRead(RX));
    bitWrite(byte_read, 7 - i, bit_read);
    delayMicroseconds(30);  //double speed mode
  }
  delayMicroseconds(0);  //optionnal delay between bytes, may be less than 1490 µs
  //  Serial.println(byte_sent, HEX);
  //  Serial.println(byte_read, HEX);
  return byte_read;
}