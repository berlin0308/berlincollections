#define F_CPU 1000000UL
#include <avr/io.h>
#include <util/delay.h>


int digit0=0,digit1=0,digit2=0;
int t=0,h=70;
int noteC3=59.6;
int noteD3=53.2;
int noteE3=47.4;
int noteF3=44.7;
int noteG3=39.9;
int noteA3=35.5;

void count(int digit0,int digit1,int digit2)
{
	for(int i=0;i<32;i++)
	{
		OCR0A=255;
		TCCR0A=0x02;
		TCCR0B=0x05; //P 1024
		
		while((TIFR0&(1<<OCF0A))==0)
		{
			show0(digit0);
			_delay_ms(2);     
			show1(digit1);
			_delay_ms(2);
			show2(digit2);
			_delay_ms(2);
		}
		TCCR0B=0x00;               
		TIFR0=TIFR0|(1<<OCF0A);      
	}
}

void BinCout()
{
	//B->input C->output
	DDRB=0b11000001;
	DDRC=0b00111110;
	//B pull up
	PORTB=0xFF;       
	// set D
	DDRD=0b11111111;
}

void BoutCin()
{
	//B->output C->input
	DDRB=0b11011111;
	DDRC=0b00100000;
	//C pull up
	PORTC=0b11011111;   // the buzzer is on PC5
	// set D
	DDRD=0b11111111;
}

void show0(int digit0)
{
	if(digit0==0)
	{
		PORTB=0b11011110;
		PORTD=0b00000001;

	}
	else if(digit0==1)
	{
		PORTB=0b11011111;
		PORTD=0b11001001;

	}
	else if(digit0==2)
	{
		PORTB=0b10011111;
		PORTD=0b00100001;

	}
	else if(digit0==3)
	{
		PORTB=0b10011111;
		PORTD=0b10000001;


	}
	else if(digit0==4)
	{
		PORTB=0b10011110;
		PORTD=0b11001001;

	}
	else if(digit0==5)
	{
		PORTB=0b10011110;
		PORTD=0b10010001;
	}
	else if(digit0==6)
	{
		PORTB=0b10011110;
		PORTD=0b00010001;

	}
	else if(digit0==7)
	{
		PORTB=0b11011110;
		PORTD=0b11000001;


	}
	else if(digit0==8)
	{
		PORTB=0b10011110;
		PORTD=0b00000001;

	}
	else if(digit0==9)
	{
		PORTB=0b10011110;
		PORTD=0b10000001;

	}
	
}

void show1(int digit1)
{
	if(digit1==0)
	{
		PORTB=0b11011110;
		PORTD=0b00000010;

	}
	else if(digit1==1)
	{
		PORTB=0b11011111;
		PORTD=0b11001010;

	}
	else if(digit1==2)
	{
		PORTB=0b10011111;
		PORTD=0b00100010;

	}
	else if(digit1==3)
	{
		PORTB=0b10011111;
		PORTD=0b10000010;


	}
	else if(digit1==4)
	{
		PORTB=0b10011110;
		PORTD=0b11001010;

	}
	else if(digit1==5)
	{
		PORTB=0b10011110;
		PORTD=0b10010010;


	}
	else if(digit1==6)
	{
		PORTB=0b10011110;
		PORTD=0b00010010;


	}
	else if(digit1==7)
	{
		PORTB=0b11011110;
		PORTD=0b11000010;


	}
	else if(digit1==8)
	{
		PORTB=0b10011110;
		PORTD=0b00000010;

	}
	else if(digit1==9)
	{
		PORTB=0b10011110;
		PORTD=0b10000010;

	}
    else if(digit1==12) //C
    {
        	PORTB=0b11011110;
        	PORTD=0b00110010;
     
    }
    else if(digit1==13) //D
        {
	PORTB=0b11011110;
	PORTD=0b00000010;
	        
        }
    else if(digit1==14) //E
        {
	PORTB=0b10011110;
	PORTD=0b00110010;
	        
        }
    else if(digit1==15) //F
    {
	PORTB=0b10011110;
	PORTD=0b01110010;
	    
    }
    else if(digit1==16) //G
    {
	PORTB=0b11011110;
	PORTD=0b00010010;
	    
    }
    else if(digit1==10) //A
    {
	   PORTB=0b10011110;
	   PORTD=0b01000010;
	    
    }
}

void show2(int digit2)
{
	if(digit2==0)
	{
		PORTB=0b01011110;
		PORTD=0b00000100;

	}
	else if(digit2==1)
	{
		PORTB=0b01011111;
		PORTD=0b11001100;

	}
	else if(digit2==2)
	{
		PORTB=0b00011111;
		PORTD=0b00100100;

	}
	else if(digit2==3)
	{
		PORTB=0b00011111;
		PORTD=0b10000100;


	}
	else if(digit2==4)
	{
		PORTB=0b00011110;
		PORTD=0b11001100;

	}
	else if(digit2==5)
	{
		PORTB=0b00011110;
		PORTD=0b10010100;


	}
	else if(digit2==6)
	{
		PORTB=0b00011110;
		PORTD=0b00010100;


	}
	else if(digit2==7)
	{
		PORTB=0b01011110;
		PORTD=0b11000100;


	}
	else if(digit2==8)
	{
		PORTB=0b00011110;
		PORTD=0b00000100;

	}
	else if(digit2==9)
	{
		PORTB=0b00011110;
		PORTD=0b10000100;

	}
	
}

void noise(int n)
{
	int t=0,c;

	if(n==noteA3)
    c=10;
    if(n==noteC3)
    c=12;
    if(n==noteD3)
    c=13;
    if(n==noteE3)
    c=14;
    if(n==noteF3)
    c=15;
    if(n==noteG3)
    c=16;

	//約t=50時約為按下按鈕的時長
	while(t<250)
	{
        show0(3);
		//關掉buzzer
		PORTC=0b00011111;  // turn on the LED when making noise
		                   // the LED will be turned off by other function outside
		//持續多久
		OCR0A=n;                   //設定n 就是代表一個數值而已
		TCCR0A=0x02;                 //CTC mode
		TCCR0B=0x03;                 //start timer p=64
		while((TIFR0&(1<<OCF0A))==0);//wait for flag
		TCCR0B=0x00;                 //stop timer
		TIFR0=TIFR0|(1<<OCF0A);      //clear timer
		
        show1(c);
		//要打開buzzer
		PORTC=0b00111111;
		
		//持續多久
		OCR0A=n;                   //設定n
		TCCR0A=0x02;                 //CTC mode
		TCCR0B=0x03;                 //start timer p=64
		while((TIFR0&(1<<OCF0A))==0);//wait for flag
		TCCR0B=0x00;                 //stop timer
		TIFR0=TIFR0|(1<<OCF0A);      //clear timer
		
		//計算總發音時長
		t++;
	}
}

int main(void)
{
	
	
	int mode=1; // initialized, watch increasing mode
    BinCout(); // set DDRx,PORTx,C output
    while(1)
    {
	    count(digit0,digit1,digit2);  // to count each second
	    t++; // increasing value
	    h--; // decreasing value
        CLKPR=(1<<CLKPCE); // clock
        CLKPR=0b00000011;
      
      if(mode==0) // piano mode
      {
	     BoutCin();
	     PORTB=0b00011100; // PB1
		 if((~PINC)&(1<<PORTB1)) // button "0" (PC4,PB1) change mode
		 {
			mode=1; // change to watch mode
			PORTB=0b11011111; // dark screen
			PORTD=0b11111000;
			_delay_ms(5000);
		 }
	     else // press C D E F B(G) A to make sound
	      {
		       BoutCin();
			   PORTB=0b00011100; // PB1 close
		       if((~PINC)&(1<<PORTC3))  // PC3
		       {
			       noise(noteA3); // button "A" (PC3,PB1)
				   PORTC=0b00011110; // close the buzzer
				   _delay_ms(10);
			   }
			   else if((~PINC)&(1<<PORTC3)) // button "B" (PC2,PB1)
			   {
				   noise(noteG3);
				   PORTC=0b00011110;
				   _delay_ms(10);
			   }
			   else if((~PINC)&((1<<PORTC3))) // button "F" (PC1,PB1)
			   {
				   noise(noteF3);
                   PORTC=0b00011110; // close the buzzer
				   _delay_ms(10);
			   }
               else
               {
				   BinCout();
				   PORTC=0b00011100; // PC1 close
				   if((~PINB)&(1<<PORTB2)) // PB2
				   {
					   noise(noteE3); // button "E" (PC1,PB2)
					   PORTC=0b00011110; // close the buzzer
					   _delay_ms(10);
				   }
				   else if(~PINB&(1<<PORTB3)) // PB3
				   {
					   noise(noteD3); // button "D" (PC1,PB3)
					   PORTC=0b00011110; // close the buzzer
					   _delay_ms(10);
				   }
				   else if(~PINB&(1<<PORTB4)) // PB4
				   {
					   noise(noteC3); // button "C" (PC1,PB4)
					   PORTC=0b00011110; // close the buzzer
					   _delay_ms(10);
				   }
				   else
				   PORTC=0b00011110; // close the buzzer
				   _delay_ms(10);
			   }
              
          }
	  }
		  else if(mode==1) // increasing watch mode
		  {
			  BinCout();
			  PORTC=0b00010110; // PC3 close
			  
			  if(digit2>=0 && digit1==0 && digit0==0) // 整點
			  {
				  PORTC=0b00011111;  // the LED 
				  _delay_ms(200);
				  
				  PORTC=0b00011110;
				  _delay_ms(200);
				  
				  PORTC=0b00011111;
				  _delay_ms(200);
			  }
			  
			  if(~PINB&(1<<PORTB3)) // PB3
			  {
				  t=0; // reset t
				  _delay_ms(500);
			  }
			  PORTC=0b00001110; // PC4 close 
			  if(~PINB&(1<<PORTB1)) // PB1
			  {
				 mode=0; // change to piano mode
				 _delay_ms(1000);
			  }
			  else if(~PINB&(1<<PORTB4)) // PB4
			  {
				  mode=2; // change to watch countdown mode
				  h=70; // reset
				  _delay_ms(1000);
			  }
			  else  // watch increasing mode
			  {
				     digit0=t%10;
				     digit1=t/10;
				     digit2=t/60;
				     digit1=digit1-digit2*6;
					 count(digit0,digit1,digit2); // including display function
			  }
		  }
		  else if(mode==2) // watch countdown mode
		  {
			  BinCout();
			  if(digit2>=0 && digit1==0 && digit0==0) // 整點
			  {
				  PORTC=0b00011111;  // the LED
				  _delay_ms(200);
				  
				  PORTC=0b00011110;
				  _delay_ms(200);
				  
				  PORTC=0b00011111;
				  _delay_ms(200);
			  }
			  
			  if(~PINB&(1<<PORTB3)) // PB3
			  {
				  h=70; // reset h
				  _delay_ms(500);
			  }
			  PORTC=0b00001110; // PC4 close
			  if(~PINB&(1<<PORTB1)) // PB1
			  {
				  mode=0; // change to piano mode
				  PORTB=0b11011111; // dark screen
				  PORTD=0b11111000;
				  _delay_ms(1000);
			  }
			  else if(~PINB&(1<<PORTB4)) // PB4
			  {
				  mode=2; // change to watch countdown mode
				  t=0; // reset
				  _delay_ms(1000);
			  }
			  else  // watch countdown mode
			  {
				  digit0=h%10;
				  digit1=h/10;
				  digit2=h/60;
				  digit1=digit1-digit2*6;
				  count(digit0,digit1,digit2); // including display function
			  }
		  }
      
   }
}