
object HelloWorld {

// Variable declarations
       val a = 5;
       val b : Int = 27,  aldo = 21;
    // Array declarations and usage   
      val c = new Array[Int](21);
       c[5] = a;
       a = c[20]*2;

    // Case switch statements
       2*c[20] + 1 match{
         case b * 2 => a = 2;
         case 7 => a = 3;
         case 2 => {a = 4; a = 6;}
       }
     // Recursive functions
        def print() = {
           val a = 2;
           print();
           return a;
       }
      // nested while loops with scopes.
       while(a >= 2) {
           print();
           a = a - 1;
           val b  = 32;
           while( b < 50) {
                  b = b + 1 ;
             }
           }

      // nested if else.

//nested if else,
   if(a ==31) {
        print();
        if(b == 5) {
             print();
        }
   }
   else {
         a = 31;
   }

   val i = 31;

// nested for loop, with scope usage and both forms.
   for ( i <- 23 to 71) {
       val j = 32;
       for ( j <- 21 until 23) a = a*2;
       print();
   }

    val d = 32;
}
