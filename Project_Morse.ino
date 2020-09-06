const int Button_pin = 2;
const int LED_pin = 13;
const int dt = 1000;
int time_on = 0;
int time_off = 0;


void setup() {
  // start serial connection
  Serial.begin(9600);

  // configure pins
  pinMode(Button_pin, INPUT_PULLUP);
  pinMode(LED_pin, OUTPUT);
}

void loop() {
  int button = !digitalRead(Button_pin);

  if (button) {   // button is active
    digitalWrite(LED_pin, HIGH);
    time_on++;
    time_off = 0;
    
  } else {       // button is inactive
    digitalWrite(LED_pin, LOW);

    if (time_on){   // button just became inactive
      if (time_on > 25){
        Serial.println("dash");
      }
      else{
        Serial.println("dot");
      }
    }
    else{
      if (time_off == 75){  // pause means the letter ended
        Serial.println("letter");
      }
    }

    time_on = 0;
    time_off ++;
  }

  delay(10);
}
