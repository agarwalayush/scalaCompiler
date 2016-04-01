import scala.collection.immuatable

object sort {

    def quicksort(arr: Array[Int]) {

        def swap(i: Int, j: Int) {
            val t = arr(i); 
            a[i] = arr(j); 
        }

        def sort(l: Int, r: Int) {
            val pivot = arr((l + r) / 2);
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

        sort(0, arr.length - 1);
    }

    def main() {
        val a = Array(4, 3, 9, 2, 0);
        quicksort(a);
    }

}
