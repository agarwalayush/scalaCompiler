
object HelloWorld {
       val a = 5;
       val b = 2;
       2*a + 1 match{
         case b * 2 => a = 2;
         case 7 => a = 3;
         case 2 => {a = 4; a = 6;}
       }
}
