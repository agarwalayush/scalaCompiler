class ABC() {
      var a = 10;
}

object foo{
    def apply() = {
      val a = new ABC();
      return a.a;
    }
}

