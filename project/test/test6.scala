object Test {
       var iter_count : Int = 0; 
       def println(a: Int) =  {
           a = a + 3;
           if( a == 10 ) {
               iter_count = iter_count + 1;
               println(a);
               return;
           }
           return;
       }
       println(7);
}