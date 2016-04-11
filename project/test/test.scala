object Test {

       def println(a : String) =  {
           return;
       }

       def main(args: Array[String]) =  {
       var a = 0;
       var b = 0;
      // for loop execution with a range
      for( a <- 1 to 3){
           var b = "Value of a: ";
           println(b);
      }

      while( a < 20 ){
         println("Value of a: ");
         a = a + 1;
      }
      val x = 2;
      var d = 2 + 3 * 910 - 1;         //no space b/w - and 1 causes problem
      if( x !=20 ){
         println("This is if statement");
          println("This is if statement");
           println("This is if statement");
      }
      else if (1) {}
      else {
         println("This is else statement");
      }
   }

}

