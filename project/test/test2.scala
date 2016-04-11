  object Rational {
         
    def gcd(a: Int, b: Int): Int = {
      if (b == 0){
        return a;
      } else{
        return b;
      }
    }
         
    val a = 3, d = 45, n =32;
    val g = gcd(a,d);
    val numer = n / g;
    val denom = d / g;
    val floater = 13;
    def this_abc(n: Int) = {
      this_abc( n - 1 );
      }

    def add(that: Int): Int = {
      val a = 32;
     return a;
   }

    def toString() = {
      val a = numer +"/"+ denom;
      return a;
    }

  }
