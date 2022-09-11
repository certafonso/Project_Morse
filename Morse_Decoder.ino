int time_on = 0;
int time_off = 0;
char letter = 0;      // the dashes (1) an dots (0)
char len_letter = 0;  // the length of the len_letter

// dictionaries for translation
// a 0 means the caracter doesn't exist and a 1 means it's not supported
char dict1[] = {'e', 't'};
char dict2[] = {'i', 'a', 'n', 'm'};
char dict3[] = {'s', 'u', 'r', 'w', 'd', 'k', 'g', 'o'};
char dict4[] = {'h', 'v', 'f', 1, 'l', 1, 'p', 'j', 'b', 'x', 'c', 'y', 'z', 'q', 1, 1};
char dict5[] = {'5', '4', 1, '3', 1, 0, 1, '2', 0, 1, '+', 0, 1, 1, 1, '1', '6', '=', '/', 0, 1, 0, 1, 0, '7', 0, 1, 1, '8', 0, '9', '0'};
char dict6[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '?', '_', 0, 0, 0, 0, '\"', 0, 0, '.', 0, 0, 0, 0, '@', 0, 0, 0, '\'', 0, 0, '-', 0, 0, 0, 0, 0, 0, 0, 0, ';', '!', 0, ')', 0, 0, 0, 0, 0, ',', 0, 0, 0, 0, ':', 0, 0, 0, 0, 0, 0, 0};

char *dict[6] = {dict1, dict2, dict3, dict4, dict5, dict6};

void loopdecode() 
{
  int button = !digitalRead(Button_pin);

  // The button is active
  if (button) {
    digitalWrite(green_pin, HIGH);
    digitalWrite(red_pin, HIGH);
    time_on++;
    time_off = 0;
    
  } 

  // The button is inactive
  else {       
    digitalWrite(green_pin, LOW);
    digitalWrite(red_pin, LOW);

    // The button just became inactive
    if (time_on){
      // makes space for new bit and increment letter length
      letter = letter << 1;
      len_letter ++;

      // If is a dash put the bit to a 1
      if (time_on > 25){
        letter++;
      }
    }
    else{
      // Pause means the letter ended, decode the word and reset letter lenght
      if (time_off == 75){
        dodecode();
        len_letter = 0;
      }
    }

    // Increment time off
    time_on = 0;
    time_off ++;
  }

  delay(10);
}

void dodecode()
{   // Decodes the letter, prints the result
    char decoded;

    // There are no letters with more than 6 symbols
    if(len_letter <= 6){
      // Decode the letter
      decoded = decode();
      
      // If decoding was sucessfull print the caracter
      if(decoded){
        if(decoded == 1){
          Serial.print("Caracter not supported");
        }
        else{
          Serial.print(decoded);  
        }

        // Light the green LED for feedback and exit
        digitalWrite(green_pin, HIGH);
        delay(100);
        digitalWrite(green_pin, LOW);
        return;
      }
      #ifdef DEBUG
      else{
        Serial.println("\nInvalid caracter");
      }
      #endif
    }
    #ifdef DEBUG
    else{
      Serial.println("\nError");
    }
    #endif

    // Something went wrong, light the red LED
    digitalWrite(red_pin, HIGH);
    delay(100);
    digitalWrite(red_pin, LOW);
}

char decode()
{   // Decodes the morse word to char
  char mask = 0;
  char i=0;

  // Creates the mask to filter bits that aren't needed
  for(i; i<len_letter; i++){
    mask += (char) round(pow(2, i));
  }

  // Apply mask
  letter = letter & mask; 

  // Use the dictionary to decode and return the character
  return dict[len_letter-1][letter];
}