#include <SPI.h>
#include <LoRa.h>
#include <Wire.h>  
#include <time.h>
#include <timer.h>

#define SCK     5    // GPIO5  -- SX1278's SCK
#define MISO    19   // GPIO19 -- SX1278's MISnO
#define MOSI    27   // GPIO27 -- SX1278's MOSI
#define SS      18   // GPIO18 -- SX1278's CS
#define RST     14   // GPIO14 -- SX1278's RESET
#define DI0     26   // GPIO26 -- SX1278's IRQ(Interrupt Request)


unsigned int counter = 0;
int count = 1;
int sum_bytes = 0;
float time_total = 0.0;
int machine_id = 1;
int polygon_id = 1;
String rssi = "RSSI --";
String packSize = "--";
int group_ids[] = {1,0,0};
int packet[60];
unsigned int f = 12;
byte message[252];
unsigned char a[sizeof(int)];
unsigned char b[sizeof(double)];

Timer sending;

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
  LoRa.setCodingRate4(5);
  LoRa.setTxPower(20);
  for(int i=0; i<60;i++){
    if (i%2==0){
      packet[i] = -123456789;
    }
    else{
      packet[i] = 123456789;
    }
    packet[i] = -123456789;
  }
  sending.setInterval(1000); 
  sending.setCallback(send_multipoly);
  sending.start();
  
}

void loop() {
  sending.update();                       
}
void send_multipoly(){
  sum_bytes = 0;
  time_total = 0.0;
  if (polygon_id<100){
      polygon_id++;
  }
  else {
    polygon_id = 1;
    count++;
  }
  int loads = 1;
  if (loads<5) {
    int id = group_ids[0]*10000 + group_ids[1]*1000 + group_ids[2]*100 + machine_id;
    int e=0;
    for (int a=1;a<=loads;a++) { //loads
      int part_id = polygon_id*100 + loads*10 + a;
      memcpy(&message[0], &id, 4);
      memcpy(&message[4], &part_id, 4);

      int c = 2;
      for(int i=0;i<60;i++){ //62
        int element = packet[i];
        memcpy(&message[4*c], &element, 4);
        c = c + 1;
        }
      clock_t begin = clock();
      LoRa.beginPacket();
      LoRa.write(message,248);
      LoRa.endPacket();
      clock_t end = clock();
      float time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
      sum_bytes = sum_bytes + 248;
      time_total = time_total + time_spent;
      }
  }
  Serial.println("1,"+String(count)+","+String(polygon_id)+","+String(sum_bytes)+","+String(time_total,5)+","+String(LoRa.rssi()));
}
