//Game boy Printer interface with Arduino, by Caleb Dennis
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// Create an instance of the OLED display
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 32
#define OLED_RESET    -1 // Reset pin not used
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// Note the display on Nano pinouts are SDA = A4 and SCK/SCL = A5
char byte_read;
bool bit_sent, bit_read;
int clk = 2;   // clock signal
int TX = 3;    // The data signal coming from the Arduino and goind to the printer (Sout on Arduino becomes Sin on the printer)
int RX = 4;    // The response bytes coming from printer going to Arduino (Sout from printer becomes Sin on the Arduino)
int LED = 13;  //to indicate a printer ready state
int BYTEOFFSET = -305; // This is the bytes offset for the feed or print margin
int BYTETOPACKET = 984; // Converts number of bytes to number of packets
int Packetcount = 0; // number of packets from total bytes

//invert TX/RX if it does not work, assuming that everything else is OK

// Declare variables for display update timing
unsigned long lastDisplayUpdate = 0; // Timer for display updates
const unsigned long displayUpdateInterval = 200; // Update every 200 ms
bool dataSent = false; // Flag to indicate if data has been sent
bool displayOne = true; // Flag to indicate if sending is displayed 

const unsigned char PROGMEM pika [] = {
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
0x00, 0x01, 0xFE, 0x00, 0x00, 0x0E, 0x01, 0xC0, 0x00, 0xD0, 0x00, 0x3C, 0x03, 0x00, 0x00, 0x03,
0x0C, 0x00, 0x00, 0x00, 0x10, 0x40, 0x00, 0x08, 0x30, 0x47, 0x03, 0x80, 0x71, 0x98, 0x30, 0x66,
0x7E, 0x80, 0x00, 0x05, 0x00, 0x00, 0x30, 0x00, 0x00, 0xB0, 0x78, 0x34, 0x01, 0x78, 0x84, 0x6A,
0x01, 0x78, 0x84, 0x78, 0x01, 0x30, 0x84, 0x30, 0x01, 0x00, 0x4F, 0x02, 0x01, 0x00, 0x34, 0x82,
0x00, 0x80, 0x04, 0x40, 0x00, 0x80, 0x02, 0x20, 0x00, 0xC0, 0x01, 0x1C, 0x00, 0x80, 0x79, 0x14,
0x00, 0x80, 0x30, 0x84, 0x00, 0x80, 0x00, 0x84, 0x01, 0x00, 0x00, 0x02, 0x01, 0x00, 0x00, 0x02,
0x01, 0x00, 0x00, 0x02, 0x01, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
};

const unsigned char PROGMEM Pokeball [] = { // This is W=16 by H=17
0x03, 0xE0, 0x0C, 0x18, 0x10, 0x04, 0x20, 0x02, 0x20, 0x02, 0x40, 0x01, 0x41, 0xC1, 0xC2, 0x21,
0xBE, 0x3E, 0xC2, 0x21, 0x41, 0xC1, 0x40, 0x01, 0x20, 0x02, 0x10, 0x04, 0x0C, 0x18, 0x03, 0xE0,
0x00, 0x00, 
};

const unsigned char PROGMEM GBPrinter [] = { // This is W=24 by H=32
0x00, 0x00, 0x00, 0x01, 0xFF, 0xFC, 0x06, 0xC0, 0x0A, 0x0C, 0xA0, 0x0A, 0x14, 0xA0, 0x0B, 0x24,
0xA0, 0x0B, 0x6C, 0xA0, 0x0B, 0xAC, 0xA0, 0x0B, 0xAC, 0xC0, 0x0B, 0xAC, 0xFF, 0xFB, 0xAC, 0x00,
0x03, 0xAF, 0xFF, 0xFF, 0xAD, 0xFF, 0xFB, 0xAD, 0x00, 0x0B, 0xED, 0xFF, 0xFB, 0xAC, 0x00, 0x03,
0xEC, 0x00, 0x03, 0xAC, 0x00, 0x03, 0xEF, 0xFF, 0xFF, 0xA8, 0x00, 0x01, 0xE8, 0x00, 0x01, 0xA8,
0x00, 0x01, 0xE8, 0xC0, 0xFD, 0xA9, 0x20, 0xA5, 0xEA, 0x10, 0xB5, 0xA9, 0x20, 0xA5, 0xA8, 0xC0,
0xFD, 0xA7, 0xFF, 0xFF, 0xB0, 0x00, 0x01, 0x9F, 0xFF, 0xFF, 0x80, 0x00, 0x01, 0x7F, 0xFF, 0xFE
};

void setup() {
  // ############################# display code ################################################
  // Initialize the display
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.println("");
  display.println("     Booting...     ");
  display.println("");
  display.drawBitmap(0,0,GBPrinter,24,32, 1);
  display.drawBitmap(95,0,pika,32,128, 1);
  display.display();
  delay(2500); // Wait for 2 second

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
  display.println("=================");
  display.println("|   GB Printer  |");
  display.println("|     READY!    |");
  display.println("=================");
  display.drawBitmap(105,8,Pokeball,16,17, 1);
  display.display();
  while (Serial.available() > 0) {  // Flush the buffer
    Serial.read();
  }
  digitalWrite(LED, HIGH); // Turn on the LED
}

// ############################## Loop for Sending Data ###############################################
void loop() {
  static unsigned long lastUpdateTime = 0; // Timer for display updates
  const unsigned long displayDuration = 1000; // Duration to show "Sending data..." in milliseconds

  if (Serial.available() > 0) {
    char data = Serial.read(); // Read the incoming byte
    Serial.write(printing(data)); // Send data to the printer
    dataSent = true; // Set the flag indicating data has been sent

    // Increment the packet counter
    Packetcount++; // Increment the packet number
    int packet = ((Packetcount - BYTEOFFSET)/BYTETOPACKET);

    // Update the display to show "Sending data" only once
    if (displayOne) {
      display.clearDisplay();
      display.setCursor(0, 0);
      display.println("     Sending data........");
      display.print("     Packet: "); // Add a label for the packet number 
      display.print(packet); // Display the packet number
      display.drawBitmap(0,0,GBPrinter,24,32, 1);
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
        display.println("=================");
        display.println("|   GB Printer  |");
        display.println("|     READY!    |");
        display.println("=================");
        display.drawBitmap(105,8,Pokeball,16,17, 1);
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
    delayMicroseconds(15);  //double speed mode
    digitalWrite(clk, HIGH);
    bit_read = (digitalRead(RX));
    bitWrite(byte_read, 7 - i, bit_read);
    delayMicroseconds(15);  //double speed mode
  }
  delayMicroseconds(0);  //optionnal delay between bytes, may be less than 1490 µs
  //  Serial.println(byte_sent, HEX);
  //  Serial.println(byte_read, HEX);
  return byte_read;
}