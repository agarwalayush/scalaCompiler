object Test {
       var anis : Int = 0; 
       def gcd(a: Int, b: Int) : Int =  {
           if( b == 0) {return a;}
           val temp = gcd(b, a%b);
           return temp;
       }
       anis = gcd(16,8);
       println(anis);
}