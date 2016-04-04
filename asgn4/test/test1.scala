
object HelloWorld {
       def print() = {
           val a = 2;
           print();
       }

       val a = 5;
  // Variable declarations
       var b = 21;

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

   if(a ==31) {
      print();
        if(b == 5) {
        print();
      }
}
      else {
         a = 31;
      }

       val d = 32;
}
