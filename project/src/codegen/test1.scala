object Test {
       def timesTwo(a: Int) =  {
           a = a*2;
           if(a < 21) {
                timesTwo(a);
           }
           return;
       }
       timesTwo(7);
}