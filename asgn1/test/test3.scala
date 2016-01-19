object example {

    abstract class Tree
    case class Node(left: Tree, right: Tree) extends Tree

    case class Leaf(x: Int) extends Tree

    val t = Node(Node(Leaf(1), Leaf(2)), Node(Leaf(11), Leaf(12)))

    def sumL(t: Tree): Int = t match {
        case Node(l, r) => sumL(l) + sumL(r)
        case Leaf(x) => x
    }

    def main(args: Array[String]) {
        println("sum of leaves = " + sumL(t))
    }
}
