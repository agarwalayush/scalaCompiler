object Test {
   def main(args: Array[String]) {
      var a = 0;
      // for loop execution with a range
      for( a <- 1 to 10){
         println( "Value of a: " + a );
      }
   }
}
object Test {
   def main(args: Array[String]) {
      var a = 0;
      // for loop execution with a range
      for( a <- 1 until 10){
         println( "Value of a: " + a );
      }
   }
}
object Test {
   def main(args: Array[String]) {
      var a = 0;
      var b = 0;
      // for loop execution with a range
      for( a <- 1 to 3; b <- 1 to 3){
         println( "Value of a: " + a );
         println( "Value of b: " + b );
      }

      while( a < 20 ){
         println( "Value of a: " + a );
         a = a + 1;
      }

      var a = 2 + 3 * 910 - 1;         //no space b/w - and 1 causes problem
      if( x !=20 ){
         println("This is if statement");
          println("This is if statement");
           println("This is if statement");
      }
      else if (1) {}
      else{
         println("This is else statement");
      }
   }

   a = func();
}


class Point(xc: Int, yc: Int) {
   var x: Int = xc;
   var y: Int = yc;

   var x = new Test () ;            // Object instance

   def move(dx: Int, dy: Int) {
      x = x + dx;
      y = y + dy;
      println ("Point x location : " + x);
      println ("Point y location : " + y);
   }
   def main(args: Array[String]) {
      val pt = new Point(10, 20);

      // Move to a new location
      pt.move(10, 10);
   }

   def matchTest(x: Int): String = {x match {
      case 1 => "one"
      case 2 => "two"
      case _ => "many"
   }
   }
/* ---------------- Not working--------------------- as y:Int not expression -------
                              def matchTest(x: Any){
                                 x match {
                                    case 1 => "one"
                                    case "two" => 2
                                    case y: Int => "scala.Int"
                                    case _ => "many"
                                 }
                              }
---------------------------------------------------*/
}

