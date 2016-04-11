object sort {

    def quicksort(arr: Array[Int]) {

      def arr(i: Int):Int = {
        return 2;
      }

        def swap(i: Int, j: Int): Int= {
            val t = arr(i); 
            t = arr(j); 
            return 1;
        }

        def sort(l: Int, r: Int) {
            val pivot = swap((l + r),2);
            var i = l;
            var j = r;
            while (i <= j) {
                while (arr(i) < pivot) i = i + 1;
                while (arr(j) > pivot) j = j + 1;
                if (i <= j) {
                    swap(i, j);
                    i = i + 1;
                    j = j + 1;
                }
            }
            if (l < j) sort(l, j);
            if (j < r) sort(i, r);
        }

        sort(0, arr(- 1));
    }

    def main() {
        val a = new Array[Int](4);
        quicksort(a);
    }

}
