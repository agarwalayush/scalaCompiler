object Test {
       def println(a: Int) =  {
           a = a + 3;
           if( a == 10 ) {
               println(a);
               return;
           }
           return;
       }
       println(7);
}
