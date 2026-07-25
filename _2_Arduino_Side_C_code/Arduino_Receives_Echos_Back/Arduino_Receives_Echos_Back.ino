// Arduino Recieves Characters from Tkinter App running on PC 
// and send backs text string 

void setup()
{
  Serial.begin(9600);
}

void loop() 
{

  // Check if data is available
  if (Serial.available() > 0)
   {
    char command;
    command = Serial.read();  // read one character

    switch (command)
    {

      case 'A':  
            Serial.println('A');  
      break;

      case 'B': 
            Serial.println('B');    
      break;

      case 'C':  
            Serial.println('C');  
      break;

      default:   // Unknown command
        Serial.println("Invalid command");
      break;

      delay(500);
    }
  }
}