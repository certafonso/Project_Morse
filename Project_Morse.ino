const int Button_pin = 2;
const int green_pin = 3;
const int red_pin = 4;
const int dt = 500;

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
  loopdecode();
  loopencode();

  delay(10);
}
