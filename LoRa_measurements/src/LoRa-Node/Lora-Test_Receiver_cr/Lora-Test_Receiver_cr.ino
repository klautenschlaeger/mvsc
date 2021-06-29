#include <SPI.h>
#include <LoRa.h>


#define SCK     5    // GPIO5  -- SX1278's SCK
#define MISO    19   // GPIO19 -- SX1278's MISnO
#define MOSI    27   // GPIO27 -- SX1278's MOSI
#define SS      18   // GPIO18 -- SX1278's CS
#define RST     14   // GPIO14 -- SX1278's RESET
#define DI0     26   // GPIO26 -- SX1278's IRQ(Interrupt Request)


int e;
int i;
int count;
int machine_id = 1;
int polygon_id = 0;
int element = 0;
String sending = "";
String coods= "";
int result[60];

byte received[255];

void setup() {
  Serial.begin(115200);
  while (!Serial);
  SPI.begin(SCK,MISO,MOSI,SS);
  LoRa.setPins(SS,RST,DI0);
  //869,4 – 869,65
  if (!LoRa.begin(8694E5)) {
    while (1);
  }
  LoRa.setSignalBandwidth(250000);
  LoRa.enableCrc();
  LoRa.onReceive(onReceive);
  LoRa.receive();
  
}

void loop() {
               
}
void onReceive(int packetSize) {
  // received a packet
  i=0;
  sending = "";
  coods= "";
  while (LoRa.available()) {
    received[i]= LoRa.read();
    i++;
  }
  //float rssi_lora = LoRa.packetRssi();
  //float snr = LoRa.packetSnr();
  e=0;
  if(i>=8){
    memcpy(&machine_id, &received[0], 4);
    memcpy(&polygon_id, &received[4], 4);
    while(e<((i-8)/4)){
      memcpy(&element, &received[e*4+8], 4);
      result[e] = element;
      e++;
    }

  }
  sending="1,"+String(machine_id)+","+ String(polygon_id)+","+ String(i)+","+ String(LoRa.packetRssi());
  count = 0;
  
  for(int a = 0; a<e;a++){
    coods= coods+"," + String(result[a]);
    count++;
  }
  
  sending = sending +","+ String(count);
  Serial.print(sending);
  Serial.println(coods);
  
}  
