#include <ncurses.h>
#include <unistd.h>

#define DELAY 35000

int
main (int argc, char *argv[])
{
  int x = 0, y = 0;

  int max_x = 0, max_y = 0;
  int next_x = 0;
  int next_y = 0;
  int direction = 1;

  initscr ();			/* Start curses mode            */
  raw ();			/* Line buffering disabled      */
  keypad (stdscr, TRUE);	/* We get F1, F2 etc..          */
  noecho ();			/* Don't echo() while we do getch */
  curs_set (FALSE);		/* Don't display a cursor */

  getmaxyx (stdscr, max_y, max_x);

  
  x = max_x / 2;
  y = max_y / 2;

  // The car cannot go everywhere on the screen
  // Remmeber: top left is (0,0)
  int min_car_x = max_x/3;
  int max_car_x = 2*max_x/3;
  int min_car_y = 0;
  int max_car_y = max_y;

  while (1)
    {

      clear ();
      for(int i = 0;i<max_y;i++){
	mvprintw (i, min_car_x, "|");
	mvprintw (i, max_car_x, "|");
      }
      mvprintw(y,x,"o");
      refresh ();

      //usleep (DELAY);


      int ch = getch ();		/* If raw() hadn't been called
				 * we have to press enter before it
				 * gets to the program          */
      switch(ch)
	{	
	case KEY_UP:
	  next_y = (y-direction);
	  if (!(next_y >= max_car_y || next_y < min_car_y )){
	    y = next_y;
	  }
	  break;
	case KEY_DOWN:
	  next_y = (y+direction);
	  if (!(next_y >= max_car_y || next_y < min_car_y)){
	    y = next_y;
	  }
	  break;
	case KEY_LEFT:
	  next_x = (x-direction);
	  if (!(next_x >=  max_car_x || next_x <=min_car_x)){
	    x = next_x;
	  }
	  break;
	case KEY_RIGHT:
	  next_x = (x+direction);
	  if (!(next_x >= max_car_x || next_x <= min_car_x)){
	    x = next_x;
	  }
	  break;
	case 27:
	  endwin ();
	  return 0;
	  break;
	}

      refresh();			/* Print it on to the real screen */
      //getch();			/* Wait for user input */


    }

  endwin ();

  return 0;
}
