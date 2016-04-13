object Test {
       def foo(i: Int) : Int = {
           i match {
             case 0 =>{return  0;}
             case 1 => {return 17;}
             }
           return 1267;
       }
       var fib_val : Int = 0;
       fib_val = foo(1);
       println(fib_val);
}