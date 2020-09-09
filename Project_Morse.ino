const int Button_pin = 2;
const int green_pin = 3;
const int red_pin = 4;
const int dt = 1000;
int time_on = 0;
int time_off = 0;
char letter = 0;      // the dashes (1) an dots (0)
char len_letter = 0;  // the length of the len_letter

// dictionaries for translation
char dict1[] = {'e', 't'};
char dict2[] = {'i', 'a', 'n', 'm'};
char dict3[] = {'s', 'u', 'r', 'w', 'd', 'k', 'g', 'o'};
char dict4[] = {'h', 'v', 'f', 'ü', 'l', 'ä', 'p', 'j', 'b', 'x', 'c', 'y', 'z', 'q', 'ö', 1};
char dict5[] = {'5', '4', 1, '3', 'é', 0, 1, '2', 0, 'è', '+', 0, 1, 'à', 1, '1', '6', '=', '/', 0, 'ç', 0, 1, 0, '7', 0, 1, 1, '8', 0, '9', '0'};
char dict6[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '?', '_', 0, 0, 0, 0, '\"', 0, 0, '.', 0, 0, 0, 0, '@', 0, 0, 0, '\'', 0, 0, '-', 0, 0, 0, 0, 0, 0, 0, 0, ';', '!', 0, ")", 0, 0, 0, 0, 0, ',', 0, 0, 0, 0, ':', 0, 0, 0, 0, 0, 0, 0};

char *dict[6] = {dict1, dict2, dict3, dict4, dict5, dict6};

void setup() 
{
  // start serial connection
  Serial.begin(9600);

  // configure pins
  pinMode(Button_pin, INPUT_PULLUP);
  pinMode(green_pin, OUTPUT);
  pinMode(red_pin, OUTPUT);
}

void loop() 
{
  int button = !digitalRead(Button_pin);

  if (button) {   // button is active
    digitalWrite(green_pin, HIGH);
    digitalWrite(red_pin, HIGH);
    time_on++;
    time_off = 0;
    
  } else {       // button is inactive
    digitalWrite(green_pin, LOW);
    digitalWrite(red_pin, LOW);

    if (time_on){   // button just became inactive
    letter = letter << 1;  // makes space for new bit
    len_letter ++;

      if (time_on > 25){  // dash (1) dot is 0, nothing is needed
        letter++;
      }
    }
    else{
      if (time_off == 75){  // pause means the letter ended
        dodecode();
        len_letter = 0;
      }
    }

    time_on = 0;
    time_off ++;
  }

  delay(10);
}

void dodecode()
{   // decodes the letter, prints the result
    char decoded;

    if(len_letter <= 6){
      decoded = decode();
      
      if(decoded){
        if(decoded == 1){
          Serial.println("Caracter not supported");
        }
        else{
          Serial.println(decoded);  
        }
        digitalWrite(green_pin, HIGH);
        delay(100);
        digitalWrite(green_pin, LOW);
        return;
      }
      else{
        Serial.println("Invalid caracter");
      }
    }
    else{
      Serial.println("Error");
    }
    digitalWrite(red_pin, HIGH);
    delay(100);
    digitalWrite(red_pin, LOW);
}

char decode()
{   // decodes the morse word to char
  char mask = 0;
  char i=0;

  for(i; i<len_letter; i++){  // creates the mask to filter bits that aren't needed
    mask += (char) round(pow(2, i));
  }

  letter = letter & mask; // apply mask

  return dict[len_letter-1][letter];
}
