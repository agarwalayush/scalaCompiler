  class Rational(n: Int, d: Int) {

    val a = require(d != 0);
    val g = gcd(n.abs, d.abs);
    val numer = n / g;
    val denom = d / g;
    val floater = 13;
    def this_abc(n: Int) = {
      this_abc(n, 1);
      }

    def add(that: Rational): Rational = {
      val a = new Rational(numer * that.denom + that.numer * denom, denom * that.denom);
     return a;
   }

    def toString() = {
      val a = numer +"/"+ denom;
      return a;
    }
    def gcd(a: Int, b: Int): Int = {
      if (b == 0){
        return a;
      } else{
        return b;
      }
    }
  }
