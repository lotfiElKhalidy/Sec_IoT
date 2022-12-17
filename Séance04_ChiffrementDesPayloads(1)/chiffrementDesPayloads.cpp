// Carte Intel curie Arduino / Genuino 101
// Ajouter les bibliothèques Ressources -> Ressources Librairies :
// Bibliothèque : Wifi ESP8266 - Arduino
// Bibliothèque : MQTT - Arduino
// Outils -> Inclure une bibliothèque -> Ajouter la bibliothèque .ZIP 

#include <SPI.h>
#include <Countdown.h>
#include <IPStack.h>
#include <MQTTClient.h>
#include <WiFiEsp.h>
#include <Base64.h>

char * Xor(char * in, int inSize, char * key, int keySize, char * out) {
	int it_key = 0;

    for (int i=0; i<inSize; i++) {
        out[i] = in[i] ^ key[it_key];
        it_key = (i + 1) % keySize;
    }
    
	return out;
}

// Variables => pins des input et output
const int led_D5 = 13;
const int led_D6 = 12;

const int bouton_S2 = 8;
const int bouton_S3 = 9;

bool ChangeLed_D5 = false; 
bool ChangeLed_D6 = false;

bool Bp_S2 = true;
bool Bp_S3 = true;

WiFiEspClient c;
IPStack ipstack(c);
MQTT::Client<IPStack, Countdown> client = MQTT::Client<IPStack, Countdown>(ipstack);

// Noms des topics
String subLED  = "\x2f\x46\x2f\x58\x27\x1a\x01\x03\x69\x79\x03\x71\x35\x1a\x65";
String subBP   = "\x2f\x46\x2f\x58\x27\x1a\x01\x03\x69\x77\x16\x46\x69\x16";
String pubBP1  = "\x2f\x46\x2f\x58\x27\x1a\x01\x03\x69\x77\x16\x46\x69\x77\x16\x04";
String pubBP2  = "\x2f\x46\x2f\x58\x27\x1a\x01\x03\x69\x77\x16\x46\x69\x77\x16\x07";
String pubLED1 = "\x2f\x46\x2f\x58\x27\x1a\x01\x03\x69\x79\x03\x71\x35\x1a\x0a\x70\x02\x04";
String pubLED2 = "\x2f\x46\x2f\x58\x27\x1a\x01\x03\x69\x79\x03\x71\x35\x1a\x0a\x70\x02\x07";

// Clé de chiffrement XOR
char key[] = "F5";
int keySize = 2;

void CallBackBpMsg(MQTT::MessageData& md) {
    MQTT::Message &message = md.message;
    MQTTString &topic = md.topicName;

    Serial.print("Message BP arrived: qos ");
    Serial.print(message.qos);
    Serial.print(", retained ");
    Serial.print(message.retained);
    Serial.print(", dup ");
    Serial.print(message.dup);
    Serial.print(", packetid ");
    Serial.println(message.id);
    
    char * topicName = new char[topic.lenstring.len+1]();
    memcpy(topicName,topic.lenstring.data,topic.lenstring.len);
    Serial.print(", topic ");
    Serial.println(topicName);
    
    char * msgPL = new char[message.payloadlen+1]();
    memcpy(msgPL,message.payload,message.payloadlen);
    Serial.print("Payload ");
    Serial.println(msgPL);

    // decode msgPL
    char msgDecoded[base64_dec_len(msgPL, sizeof(msgPL))];
    base64_decode(msgDecoded, msgPL, sizeof(msgPL));

    if (!strncmp(&topic.lenstring.data[topic.lenstring.len-3],"BP1",3)) {
        if (!strncmp(msgDecoded,"ON",2)) {
            ChangeLed_D6 = true;
        }
    }
    if (!strncmp(&topic.lenstring.data[topic.lenstring.len-3],"BP2",3)) {
        if (!strncmp(msgDecoded,"ON",2)) {
            ChangeLed_D5 = true;
        }
    }

    delete msgPL;
    delete topicName;
}

void CallBackLedMsg(MQTT::MessageData& md) {
    MQTT::Message &message  = md.message;
    MQTTString &topic = md.topicName;
    
    Serial.print("Message LED arrived: qos ");
    Serial.print(message.qos);
    Serial.print(", retained ");
    Serial.print(message.retained);
    Serial.print(", dup ");
    Serial.print(message.dup);
    Serial.print(", packetid ");
    Serial.println(message.id);

    char * topicName = new char[topic.lenstring.len+1]();
    memcpy(topicName,topic.lenstring.data,topic.lenstring.len);
    Serial.print(", topic ");
    Serial.println(topicName);
    
    char * msgPL = new char[message.payloadlen+1]();
    memcpy(msgPL,message.payload,message.payloadlen);
    Serial.print("Payload ");
    Serial.println(msgPL);

    // decode msgPL
    char msgDecoded[base64_dec_len(msgPL, sizeof(msgPL))];
    base64_decode(msgDecoded, msgPL, sizeof(msgPL));

    if (!strncmp(&topic.lenstring.data[topic.lenstring.len-4],"LED1",4)) {
        if (!strncmp(msgDecoded,"ON",2))
            digitalWrite(led_D6,HIGH);
        else
            digitalWrite(led_D6,LOW);
    }  

    if (!strncmp(&topic.lenstring.data[topic.lenstring.len-4],"LED2",4)) {
        if (!strncmp(msgDecoded,"ON",2))
            digitalWrite(led_D5,HIGH);
        else
            digitalWrite(led_D5,LOW);
    }

    delete msgPL;
    delete topicName;
}

void WifiConnect() {
    Serial1.begin(9600);
    while(!Serial1);
    Serial.begin(9600);
    while(!Serial);
    WiFi.init(&Serial1);
    WiFi.begin((char*)"ZZ_HSH","WIFI_ZZ_F5");  // paramètres : * SSID_Wifi: ZZ_HSH 
                                                  // * mot_de_passe: ZZ_HSH_F5
}

void BrokerConnect() {
    MQTTPacket_connectData configMQTT = MQTTPacket_connectData_initializer;
    
    configMQTT.clientID.cstring = (char*)"GROUPE_06";
    configMQTT.username.cstring = (char*)"";
    configMQTT.password.cstring = (char*)"";
    configMQTT.willFlag = 0;

    ipstack.connect((char *)"192.1668.1.136", 1883);  // paramètres : adresseIP_du_broker et port

    int rc = client.connect(configMQTT);
    
    if(rc == 0)
        Serial.println("Connected OK");
    else
        Serial.println("Not Connected ERROR");

    client.subscribe(subBP.c_str(), MQTT::QOS0, CallBackBpMsg);
    client.subscribe(subLED.c_str(),MQTT::QOS0, CallBackLedMsg);
}

void PortsSetup() {
    // initialisation des broches 12 et 13 comme étant des sorties
    pinMode(led_D5, OUTPUT);
    pinMode(led_D6, OUTPUT);
    // initialisation des broches 8 et 9 comme étant des entrées
    pinMode(bouton_S2, INPUT);
    pinMode(bouton_S3, INPUT);
}

void setup() {
    WifiConnect();
    BrokerConnect();
    PortsSetup();
}

// Intéret de ce code : Si on appuie sur un bouton pussoir, la LED qui y est associé s'allume 
void loop() {
    // decode "ON" and "OFF"
    char on[]  = "ON";
    char off[] = "OFF";

    char encodedOn[base64_enc_len(sizeof(on))];
    char encodedOff[base64_enc_len(sizeof(off))];

    base64_encode(encodedOn, on, sizeof(on));
    base64_encode(encodedOff, off, sizeof(off));

    client.yield(100);

    if (Bp_S2 != digitalRead(bouton_S2)) {
        Bp_S2 = !Bp_S2;
        MQTT::Message message;
        message.qos = MQTT::QOS0;
        message.retained = false;
        message.payload = (void *)(Bp_S2? encodedOff : encodedOn);
        message.payloadlen = strlen(Bp_S2? encodedOff :encodedOn);
        client.publish(Xor(pubPB1, sizeof(pubPB1), key, tmp), message);
    }

    if (Bp_S3 != digitalRead(bouton_S3)) {
        Bp_S3 = !Bp_S3;
        MQTT::Message message;
        message.qos = MQTT::QOS0;
        message.retained = false;
        message.payload = (void *)(Bp_S3? encodedOff : encodedOn);
        message.payloadlen = strlen(Bp_S3? encodedOff : encodedOn);
        client.publish(Xor(pubPB2, sizeof(pubPB2), key, tmp),message);
    }

    if (ChangeLed_D6) {
        MQTT::Message message;
        message.qos = MQTT::QOS0;
        message.retained = true;
        message.payload = (void *)(!digitalRead(led_D6)? encodedOn : encodedOff);
        message.payloadlen = strlen(!digitalRead(led_D6)? encodedOn : encodedOff);
        client.publish(Xor(pubLED1, sizeof(pubLED1), key, tmp), message);
        ChangeLed_D6 = false;
    }

    if (ChangeLed_D5) {
        MQTT::Message message;
        message.qos = MQTT::QOS0;
        message.retained = true;
        message.payload = (void *)(!digitalRead(led_D5)? encodedOn : encodedOff);
        message.payloadlen = strlen(!digitalRead(led_D5)? encodedOn : encodedOff);
        client.publish(Xor(pubLED2, sizeof(pubLED2), key, tmp), message);
        ChangeLed_D5 = false;
    }
}