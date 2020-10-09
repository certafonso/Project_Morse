char incomingByte = 0;
const int green_pin = 3;
const int red_pin = 4;
const int dt = 500;

// first 3 bits are the lenght of the character and the rest are the dots (0) and dashes (1)
char encode_dict[] = {66, 132, 164, 131, 1, 36, 195, 4, 2, 116, 163, 68, 194, 130, 227, 100, 212, 67, 3, 129, 35, 20, 99, 148, 180, 196, 253, 125, 61, 29, 13, 5, 133, 197, 229, 245};

void setup() 
{
  // start serial connection
  Serial.begin(9600);

  pinMode(green_pin, OUTPUT);
  pinMode(red_pin, OUTPUT);
}

void loop() 
{
  // send data only when you receive data:
  if (Serial.available() > 0) {
    // read the incoming byte:
    incomingByte = Serial.read();

    Serial.print("I received: ");
    Serial.println(incomingByte);

    transmitchar(encondebyte(incomingByte));
  }
}

char encondebyte(char byte)
{
  if(byte >= 'a' && byte <= 'z'){
    byte -= 'a';
  }
  else if(byte >= 'A' && byte <= 'Z'){
    byte -= 'A';
  }
  else if(byte >= '0' && byte <= '9'){
    byte -= '0';
    byte += 26; // numbers start at position 26
  }
  else if(byte == ' '){
    return 0;
  }
  else{
    return -1;
  }

  return encode_dict[byte];
}

void transmitchar(char word)
{ // transmits the character in morse
  char lenght = word & 7;   // masks the 5 most significant bits
  char mask = 128;
  char i;

  switch (word)
  {
  case -1:  // error
    digitalWrite(red_pin, HIGH);
    delay(dt);
    digitalWrite(red_pin, LOW);
    break;

  case 0:   // space 7* dt (4 now + 3 at the end of the function)
    delay(4*dt);
    break;
  
  default:
    for(i=0; i<lenght; i++){

      digitalWrite(green_pin, HIGH);

      if(word & mask){ // dash
        delay(3*dt);
      }
      else{   // dot
        delay(dt);
      }

      digitalWrite(green_pin, LOW);

      delay(dt);

      mask = mask >> 1;
    }
    break;
  }
  delay(3*dt); // space between caracters
}
